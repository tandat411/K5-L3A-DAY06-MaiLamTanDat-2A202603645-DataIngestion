"""Read and normalize source data using PyMuPDF."""
import logging
import re
import unicodedata
from pathlib import Path
from .models import DocumentPage

try:
    import pymupdf
except ImportError:
    pymupdf = None

logger = logging.getLogger(__name__)


def normalize_text(text: str) -> str:
    """Normalize Unicode and whitespace without discarding useful structure."""
    if not text:
        return ""

    # 1. Normalize Unicode to NFC (canonical composition - essential for Vietnamese diacritics)
    text = unicodedata.normalize("NFC", text)

    # 2. Normalize line endings, non-breaking spaces and exotic semicolons
    text = (
        text.replace("\xa0", " ")
        .replace("\u037e", ";")
        .replace("\r\n", "\n")
        .replace("\r", "\n")
    )

    # 3. Collapse multiple horizontal spaces and tabs on a single line
    text = re.sub(r"[ \t]+", " ", text)

    # 4. Remove whitespace around newlines
    text = re.sub(r" ?\n ?", "\n", text)

    # 5. Collapse 3+ newlines into 2 (preserve clean paragraph boundaries)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def load_pdf(
    path: Path | str,
    document_id: str,
    source: str,
    base_metadata: dict | None = None,
) -> list[DocumentPage]:
    """Extract each physical page using PyMuPDF; keep its page number and source.

    Extracts text blocks preserving paragraph structure.
    Detects and records pages with no text.
    """
    file_path = Path(path)
    if not file_path.exists():
        raise FileNotFoundError(f"PDF file not found: {file_path}")

    if pymupdf is None:
        raise ImportError(
            "PyMuPDF is not installed. Please install it using: pip install pymupdf"
        )

    doc = pymupdf.open(str(file_path))
    pages: list[DocumentPage] = []
    empty_pages: list[int] = []
    current_chapter: str | None = None

    try:
        for idx in range(len(doc)):
            pdf_page = doc[idx]
            physical_page = idx + 1  # 1-based physical page number

            # Extract text blocks: (x0, y0, x1, y1, text, block_no, block_type)
            # block_type == 0 is text, block_type == 1 is image
            blocks = pdf_page.get_text("blocks")
            text_blocks = [
                b[4].strip() for b in blocks if b[6] == 0 and b[4].strip()
            ]

            raw_text = (
                "\n\n".join(text_blocks)
                if text_blocks
                else (pdf_page.get_text("text") or "")
            )
            clean_text = normalize_text(raw_text)

            has_text = len(clean_text) > 0
            if not has_text:
                empty_pages.append(physical_page)

            # Detect chapter heading (e.g., Chương I, Chương III)
            chapter_match = re.search(r"Chương\s+([IVXLCDM]+)", clean_text, re.IGNORECASE)
            if chapter_match:
                current_chapter = chapter_match.group(1).upper()

            page_meta = dict(base_metadata or {})
            page_meta.update({
                "has_text": has_text,
                "char_count": len(clean_text),
                "image_count": len(pdf_page.get_images()),
            })
            if current_chapter:
                page_meta["chapter"] = current_chapter

            pages.append(
                DocumentPage(
                    document_id=document_id,
                    source=source,
                    page=physical_page,
                    text=clean_text,
                    metadata=page_meta,
                )
            )
    finally:
        doc.close()

    if empty_pages:
        logger.warning(
            "Document '%s' has %d / %d pages with no extractable text: %s",
            document_id,
            len(empty_pages),
            len(pages),
            empty_pages[:10] if len(empty_pages) > 10 else empty_pages,
        )

    return pages
