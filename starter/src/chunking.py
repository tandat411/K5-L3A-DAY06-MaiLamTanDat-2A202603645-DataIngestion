"""Implement fixed-size and structure-aware chunking."""
from .models import Chunk, DocumentPage


def fixed_size(page: DocumentPage, size: int = 500, overlap: int = 50) -> list[Chunk]:
    """Split text into overlapping windows and retain page metadata.

    Args:
        page: DocumentPage containing source text and metadata.
        size: Target chunk size in characters.
        overlap: Character overlap between consecutive chunks (must be < size).

    Returns:
        List of deterministic Chunk objects.
    """
    text = (page.text or "").strip()
    if not text:
        return []

    if overlap >= size:
        overlap = max(0, size // 2)

    step = max(1, size - overlap)
    chunks: list[Chunk] = []
    chunk_idx = 0

    for start in range(0, len(text), step):
        end = min(start + size, len(text))
        chunk_text = text[start:end].strip()
        if chunk_text:
            chunk_id = f"{page.document_id}_p{page.page}_fix_{chunk_idx}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=chunk_text,
                    metadata=dict(page.metadata),
                )
            )
            chunk_idx += 1

        if end >= len(text):
            break

    return chunks


def by_paragraph(page: DocumentPage, max_size: int = 800) -> list[Chunk]:
    """Group paragraphs, split oversized paragraphs and retain metadata.

    Args:
        page: DocumentPage containing source text and metadata.
        max_size: Maximum allowed chunk size in characters.

    Returns:
        List of structure-aware Chunk objects.
    """
    text = (page.text or "").strip()
    if not text:
        return []

    raw_paragraphs = [p.strip() for p in text.split("\n\n") if p.strip()]
    if not raw_paragraphs:
        raw_paragraphs = [text]

    # Normalize: split any single paragraph exceeding max_size into sub-chunks
    normalized_paragraphs: list[str] = []
    for p in raw_paragraphs:
        if len(p) <= max_size:
            normalized_paragraphs.append(p)
        else:
            # Sub-split oversized paragraphs cleanly
            for i in range(0, len(p), max_size):
                sub = p[i : i + max_size].strip()
                if sub:
                    normalized_paragraphs.append(sub)

    chunks: list[Chunk] = []
    current_batch: list[str] = []
    current_length = 0
    chunk_idx = 0

    for p in normalized_paragraphs:
        # Check if adding this paragraph exceeds max_size (+2 chars for \n\n)
        sep_len = 2 if current_batch else 0
        if current_batch and (current_length + sep_len + len(p) > max_size):
            chunk_text = "\n\n".join(current_batch).strip()
            chunk_id = f"{page.document_id}_p{page.page}_para_{chunk_idx}"
            chunks.append(
                Chunk(
                    chunk_id=chunk_id,
                    document_id=page.document_id,
                    source=page.source,
                    page=page.page,
                    text=chunk_text,
                    metadata=dict(page.metadata),
                )
            )
            chunk_idx += 1
            current_batch = [p]
            current_length = len(p)
        else:
            current_batch.append(p)
            current_length += sep_len + len(p)

    if current_batch:
        chunk_text = "\n\n".join(current_batch).strip()
        chunk_id = f"{page.document_id}_p{page.page}_para_{chunk_idx}"
        chunks.append(
            Chunk(
                chunk_id=chunk_id,
                document_id=page.document_id,
                source=page.source,
                page=page.page,
                text=chunk_text,
                metadata=dict(page.metadata),
            )
        )

    return chunks
