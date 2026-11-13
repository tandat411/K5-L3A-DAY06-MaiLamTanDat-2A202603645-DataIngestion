"""Orchestrate the Day 06 Data Ingestion, Retrieval and Benchmark Pipeline."""
import argparse
import csv
import json
import logging
import os
import sys
import time
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("pipeline")

# Support both module and direct script execution
starter_dir = Path(__file__).resolve().parent.parent
if str(starter_dir) not in sys.path:
    sys.path.insert(0, str(starter_dir))

try:
    from .models import Chunk, DocumentPage
    from .ingestion import load_pdf
    from .chunking import fixed_size, by_paragraph
    from .embeddings import MyEmbedder
    from .store import PgVectorStore
    from .evaluation import evaluate_query, summarize
except ImportError:
    from src.models import Chunk, DocumentPage
    from src.ingestion import load_pdf
    from src.chunking import fixed_size, by_paragraph
    from src.embeddings import MyEmbedder
    from src.store import PgVectorStore
    from src.evaluation import evaluate_query, summarize


def find_default_corpus(project_root: Path) -> Path | None:
    candidates = [
        project_root / "starter" / "data" / "LuatLaoDong2019.pdf",
        project_root / "data" / "corpus.pdf",
    ]
    for p in candidates:
        if p.exists():
            return p
    # Search for any PDF in data folders
    for d in [project_root / "starter" / "data", project_root / "data"]:
        if d.exists():
            pdfs = list(d.glob("*.pdf"))
            if pdfs:
                return pdfs[0]
    return None


def find_default_benchmark(project_root: Path) -> Path | None:
    candidates = [
        project_root / "benchmark" / "questions.json",
        project_root / "starter" / "data" / "benchmark.json",
        project_root / "data" / "benchmark.json",
    ]
    for p in candidates:
        if p.exists():
            return p
    return None


def load_benchmark(path: Path) -> list[dict[str, Any]]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    if isinstance(data, dict) and "questions" in data:
        return data["questions"]
    elif isinstance(data, list):
        return data
    raise ValueError(f"Unrecognized benchmark format in {path}")


def update_experiment_log(csv_path: Path, summary: dict[str, Any], embedder_name: str) -> None:
    """Update artifacts/experiment_log.csv with the latest benchmark metrics."""
    if not csv_path.exists():
        return

    try:
        rows = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            fieldnames = reader.fieldnames or []
            rows = list(reader)

        for row in rows:
            strat_key = f"Strategy_{row.get('strategy')}"
            strat_data = summary.get(strat_key, {})
            dev = strat_data.get("dev", {})
            test = strat_data.get("test", {})

            if dev:
                row["dev_hit1"] = dev.get("hit_at_1_ratio", "")
                row["dev_hit3"] = dev.get("hit_at_3_ratio", "")
            if test:
                row["test_hit1"] = test.get("hit_at_1_ratio", "")
                row["test_hit3"] = test.get("hit_at_3_ratio", "")

            if not row.get("vectorizer"):
                row["vectorizer"] = embedder_name

        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)
        logger.info("Updated %s with benchmark metrics.", csv_path)
    except Exception as e:
        logger.warning("Could not update experiment log: %s", e)


def main() -> None:
    parser = argparse.ArgumentParser(description="Day 06 Data Ingestion & Benchmark Pipeline")
    parser.add_argument("--corpus", type=str, default=None, help="Path to input corpus PDF")
    parser.add_argument("--benchmark", type=str, default=None, help="Path to benchmark JSON")
    parser.add_argument("--min-pages", type=int, default=30, help="Minimum required content pages")
    parser.add_argument("--top-k", type=int, default=3, help="Top-k hits to retrieve")
    parser.add_argument("--results-dir", type=str, default="starter/results", help="Directory for output traces")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent.parent

    # 1. Locate and validate corpus
    corpus_path = Path(args.corpus) if args.corpus else find_default_corpus(project_root)
    if not corpus_path or not corpus_path.exists():
        logger.error("Corpus PDF not found. Please provide --corpus <path_to_pdf>")
        sys.exit(1)

    logger.info("==================================================")
    logger.info("DAY 06 · DATA INGESTION & BENCHMARK PIPELINE")
    logger.info("==================================================")
    logger.info("Loading corpus: %s", corpus_path)

    doc_id = corpus_path.stem
    source_name = corpus_path.name
    pages = load_pdf(corpus_path, document_id=doc_id, source=source_name)

    content_pages = [p for p in pages if p.metadata.get("has_text") and p.metadata.get("char_count", 0) > 0]
    total_physical = len(pages)
    total_content = len(content_pages)
    logger.info("Extracted %d physical pages (%d pages with useful text)", total_physical, total_content)

    if total_content < args.min_pages:
        logger.warning(
            "⚠️ Corpus has %d content pages, which is less than the required %d pages! "
            "(Ensure the PDF contains a digital text layer rather than un-OCRed raster images)",
            total_content,
            args.min_pages,
        )

    # 2. Build Chunks for Strategy A and Strategy B/C
    logger.info("--------------------------------------------------")
    logger.info("Chunking strategies:")

    # Strategy A: Fixed-size 500 chars, 50 overlap
    t0_chunk = time.perf_counter()
    chunks_A: list[Chunk] = []
    for p in content_pages:
        chunks_A.extend(fixed_size(p, size=500, overlap=50))
    logger.info("  Strategy A (fixed-size 500/50): %d chunks", len(chunks_A))

    # Strategy B & C: by paragraph, max 800 chars
    chunks_B: list[Chunk] = []
    for p in content_pages:
        chunks_B.extend(by_paragraph(p, max_size=800))
    logger.info("  Strategy B/C (structure-aware <=800): %d chunks", len(chunks_B))
    t_chunk_elapsed = time.perf_counter() - t0_chunk

    # 3. Embedding and Vector Storage
    logger.info("--------------------------------------------------")
    logger.info("Initializing Embedder & Vector Store...")
    embedder = MyEmbedder()
    logger.info("Embedder: %s (Provider: %s, Dimensions: %d)", embedder.model_name, embedder.provider, embedder.dimensions)

    db_url = os.getenv("DATABASE_URL", "postgresql://day6:day6_local_only@127.0.0.1:55433/day6_lab")
    store = PgVectorStore(database_url=db_url, dimensions=embedder.dimensions)
    store.create_schema()

    if not content_pages:
        logger.error("No content pages available to embed. Aborting pipeline.")
        sys.exit(1)

    # Embed and upsert Strategy A
    logger.info("Embedding %d chunks for Strategy A...", len(chunks_A))
    t0_embed_a = time.perf_counter()
    texts_A = [c.text for c in chunks_A]
    vecs_A = embedder.embed_documents(texts_A)
    store.upsert(strategy="Strategy_A", chunks=chunks_A, vectors=vecs_A)
    time_A = time.perf_counter() - t0_embed_a
    logger.info("Strategy A stored (%d chunks in %.2fs)", len(chunks_A), time_A)

    # Embed and upsert Strategy B
    logger.info("Embedding %d chunks for Strategy B...", len(chunks_B))
    t0_embed_b = time.perf_counter()
    texts_B = [c.text for c in chunks_B]
    vecs_B = embedder.embed_documents(texts_B)
    store.upsert(strategy="Strategy_B", chunks=chunks_B, vectors=vecs_B)
    time_B = time.perf_counter() - t0_embed_b
    logger.info("Strategy B stored (%d chunks in %.2fs)", len(chunks_B), time_B)

    # Strategy C reuses Strategy B storage index with metadata filtering

    # 4. Benchmark Execution
    benchmark_path = Path(args.benchmark) if args.benchmark else find_default_benchmark(project_root)
    if not benchmark_path or not benchmark_path.exists():
        logger.warning(
            "Benchmark questions file not found! Looked in: benchmark/questions.json, starter/data/benchmark.json. "
            "Skipping retrieval evaluation. Create questions to run benchmark."
        )
        return

    logger.info("--------------------------------------------------")
    logger.info("Running Benchmark against %s...", benchmark_path)
    questions = load_benchmark(benchmark_path)
    logger.info("Loaded %d benchmark questions.", len(questions))

    all_traces: list[dict[str, Any]] = []
    filter_compliance_count = 0
    filter_total_count = 0

    t0_bench = time.perf_counter()
    for q_idx, q in enumerate(questions):
        q_text = q.get("question", "")
        q_filter = q.get("filter")
        q_vec = embedder.embed_query(q_text)

        # Strategy A search
        hits_A = store.search(strategy="Strategy_A", query_vector=q_vec, top_k=args.top_k)
        trace_A = evaluate_query(q, hits_A, strategy="Strategy_A")
        all_traces.append(trace_A)

        # Strategy B search
        hits_B = store.search(strategy="Strategy_B", query_vector=q_vec, top_k=args.top_k)
        trace_B = evaluate_query(q, hits_B, strategy="Strategy_B")
        all_traces.append(trace_B)

        # Strategy C search: uses Strategy B vectors with filters applied
        if q_filter:
            filter_total_count += 1
            hits_C = store.search(strategy="Strategy_B", query_vector=q_vec, top_k=args.top_k, filters=q_filter)
            # Verify filter compliance: do returned chunks satisfy the filter?
            compliant = True
            for h in hits_C:
                h_meta = h.get("metadata", {})
                for fk, fv in q_filter.items():
                    if str(h_meta.get(fk, "")).lower() != str(fv).lower() and str(h.get(fk, "")).lower() != str(fv).lower():
                        compliant = False
            if compliant and hits_C:
                filter_compliance_count += 1
        else:
            hits_C = store.search(strategy="Strategy_B", query_vector=q_vec, top_k=args.top_k)

        trace_C = evaluate_query(q, hits_C, strategy="Strategy_C")
        all_traces.append(trace_C)

    bench_time = time.perf_counter() - t0_bench

    # 5. Summarize Results
    summary = summarize(all_traces)
    
    # Enrich summary with system metadata and resource metrics
    summary["_metadata"] = {
        "corpus_path": str(corpus_path),
        "total_physical_pages": total_physical,
        "total_content_pages": total_content,
        "embedder": {
            "model_name": embedder.model_name,
            "provider": embedder.provider,
            "dimensions": embedder.dimensions,
        },
        "resources": {
            "Strategy_A": {
                "chunk_count": len(chunks_A),
                "embed_time_seconds": round(time_A, 2),
                "cost_usd": 0.0,
            },
            "Strategy_B": {
                "chunk_count": len(chunks_B),
                "embed_time_seconds": round(time_B, 2),
                "cost_usd": 0.0,
            },
            "Strategy_C": {
                "chunk_count": len(chunks_B),
                "embed_time_seconds": round(time_B, 2),
                "cost_usd": 0.0,
            },
        },
        "benchmark_eval_time_seconds": round(bench_time, 2),
        "filter_compliance": {
            "count": filter_compliance_count,
            "total": filter_total_count,
            "ratio": f"{filter_compliance_count}/{filter_total_count}" if filter_total_count > 0 else "N/A",
            "pct": f"{(filter_compliance_count / filter_total_count) * 100:.1f}%" if filter_total_count > 0 else "N/A",
        },
    }

    results_dir = project_root / args.results_dir
    results_dir.mkdir(parents=True, exist_ok=True)
    root_results_dir = project_root / "results"
    root_results_dir.mkdir(parents=True, exist_ok=True)

    # Save raw traces and summary
    traces_file = results_dir / "traces.json"
    summary_file = results_dir / "summary.json"

    with open(traces_file, "w", encoding="utf-8") as f:
        json.dump(all_traces, f, ensure_ascii=False, indent=2)

    with open(summary_file, "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    # Mirror to root results directory
    with open(root_results_dir / "traces.json", "w", encoding="utf-8") as f:
        json.dump(all_traces, f, ensure_ascii=False, indent=2)

    with open(root_results_dir / "summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    logger.info("Saved traces to: %s", traces_file)
    logger.info("Saved summary to: %s", summary_file)

    # Prepare Coherence & Grounding manual audit samples
    # 10 fixed locations for Coherence: sample 10 page numbers
    sample_pages = sorted(list({p.page for p in content_pages}))[:10]
    coherence_samples = []
    for p_num in sample_pages:
        c_a = [c for c in chunks_A if c.page == p_num][:1]
        c_b = [c for c in chunks_B if c.page == p_num][:1]
        coherence_samples.append({
            "page": p_num,
            "chunk_A": c_a[0].text if c_a else "",
            "chunk_B": c_b[0].text if c_b else "",
            "label_A": None,  # 0, 1, or 2 to be filled manually
            "label_B": None,
            "notes": "",
        })
    with open(results_dir / "coherence_samples.json", "w", encoding="utf-8") as f:
        json.dump(coherence_samples, f, ensure_ascii=False, indent=2)
    with open(root_results_dir / "coherence_samples.json", "w", encoding="utf-8") as f:
        json.dump(coherence_samples, f, ensure_ascii=False, indent=2)

    # 5 test questions for Grounding audit
    test_traces = [t for t in all_traces if t.get("split") == "test"]
    test_q_ids = sorted(list({t["question_id"] for t in test_traces}))[:5]
    grounding_samples = []
    for qid in test_q_ids:
        q_items = [t for t in test_traces if t["question_id"] == qid]
        grounding_samples.append({
            "question_id": qid,
            "question": q_items[0]["question"],
            "evidence_quote": q_items[0]["evidence_quote"],
            "strategies": {
                t["strategy"]: {
                    "matched_rank": t["matched_rank"],
                    "top_3_chunks": [h["text"] for h in t["hits"][:3]],
                    "grounding_score": None,  # 0, 1, or 2 to be filled manually
                    "reason": "",
                }
                for t in q_items
            },
        })
    with open(results_dir / "grounding_samples.json", "w", encoding="utf-8") as f:
        json.dump(grounding_samples, f, ensure_ascii=False, indent=2)
    with open(root_results_dir / "grounding_samples.json", "w", encoding="utf-8") as f:
        json.dump(grounding_samples, f, ensure_ascii=False, indent=2)

    # Update experiment_log.csv
    exp_log_path = project_root / "artifacts" / "experiment_log.csv"
    update_experiment_log(exp_log_path, summary, embedder.model_name)

    # Print Report Table
    print("\n" + "=" * 80)
    print("DAY 06 BENCHMARK EVALUATION REPORT")
    print("=" * 80)
    print(f"{'Strategy':<12} | {'Split':<6} | {'Hit@1 (n/N)':<12} | {'Hit@3 (n/N)':<12} | {'Hit@3 %':<8}")
    print("-" * 60)
    for strat in sorted(summary.keys()):
        for split in ["dev", "test", "all"]:
            s = summary[strat].get(split, {})
            h1 = s.get("hit_at_1_ratio", "N/A")
            h3 = s.get("hit_at_3_ratio", "N/A")
            pct = s.get("hit_at_3_pct", "N/A")
            print(f"{strat:<12} | {split:<6} | {h1:<12} | {h3:<12} | {pct:<8}")
        print("-" * 60)

    if filter_total_count > 0:
        compliance_pct = (filter_compliance_count / filter_total_count) * 100
        print(f"\nMetadata Filter Compliance (Strategy C): {filter_compliance_count}/{filter_total_count} ({compliance_pct:.1f}%)")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
