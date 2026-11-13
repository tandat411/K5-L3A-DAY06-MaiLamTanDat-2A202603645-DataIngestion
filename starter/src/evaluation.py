"""Evaluate retrieved evidence and preserve per-query traces."""
import string
from typing import Any

_PUNCT_TABLE = str.maketrans("", "", string.punctuation + "“”‘’«»–—…;\u037e\xa0")


def _normalize(text: str | None) -> str:
    """Normalize punctuation, whitespace and lowercase for reliable matching."""
    if not text:
        return ""
    # Replace non-breaking spaces and exotic semicolons
    cleaned = text.replace("\xa0", " ").replace("\u037e", ";")
    clean = cleaned.translate(_PUNCT_TABLE).lower()
    return " ".join(clean.split())


def _is_valid_hit(question: dict[str, Any], hit: dict[str, Any]) -> bool:
    """Check if a retrieved chunk matches gold document, page, and contains gold evidence."""
    hit_text_norm = _normalize(hit.get("text", ""))
    if not hit_text_norm:
        return False

    # 1. Check Document / Source ID
    gold_source = question.get("gold_source_id") or question.get("gold_source")
    if gold_source:
        hit_doc = hit.get("document_id") or hit.get("source") or ""
        if isinstance(gold_source, list):
            if not any(str(src) in str(hit_doc) for src in gold_source):
                return False
        else:
            if str(gold_source) not in str(hit_doc):
                return False

    # 2. Check Page
    gold_page = question.get("gold_page")
    if gold_page is not None:
        hit_page = hit.get("page")
        if isinstance(gold_page, list):
            if hit_page not in gold_page:
                return False
        else:
            if hit_page != gold_page:
                return False

    # 3. Check Gold Evidence Quote (accepts string or list of alternative quotes)
    evidence = question.get("evidence_quote") or question.get("evidence")
    if evidence:
        if isinstance(evidence, list):
            matches_any = any(_normalize(e) in hit_text_norm for e in evidence if e)
            if not matches_any:
                return False
        else:
            if _normalize(evidence) not in hit_text_norm:
                return False

    return True


def evaluate_query(question: dict[str, Any], hits: list[dict[str, Any]], strategy: str = "") -> dict[str, Any]:
    """Check source/page and enough gold evidence; keep hit@1 and hit@3 trace.

    Accept any documented alternative gold evidence. Do not infer human grounding
    or chunk coherence labels from exact string match.
    """
    matched_rank: int | None = None
    hit_flags: list[bool] = []

    for idx, hit in enumerate(hits):
        valid = _is_valid_hit(question, hit)
        hit_flags.append(valid)
        if valid and matched_rank is None:
            matched_rank = idx + 1  # 1-based rank

    hit_at_1 = bool(hit_flags and hit_flags[0])
    hit_at_3 = any(hit_flags[:3])

    strat_name = strategy or question.get("strategy") or (hits[0].get("strategy") if hits else "default")

    return {
        "question_id": question.get("id"),
        "question": question.get("question"),
        "split": question.get("split", "dev"),
        "strategy": strat_name,
        "hit_at_1": hit_at_1,
        "hit_at_3": hit_at_3,
        "matched_rank": matched_rank,
        "gold_source_id": question.get("gold_source_id"),
        "gold_page": question.get("gold_page"),
        "evidence_quote": question.get("evidence_quote"),
        "hits": hits,
    }


def summarize(traces: list[dict[str, Any]]) -> dict[str, Any]:
    """Aggregate Hit@1 and Evidence Hit@3 by strategy and dev/test split.

    Reports count, ratios (e.g. 12/15), and percentages as required by the rubric.
    """
    if not traces:
        return {}

    # Group traces by (strategy, split)
    grouped: dict[tuple[str, str], list[dict[str, Any]]] = {}
    strategies: set[str] = set()

    for t in traces:
        strat = t.get("strategy", "default")
        split = t.get("split", "dev")
        strategies.add(strat)
        grouped.setdefault((strat, split), []).append(t)
        grouped.setdefault((strat, "all"), []).append(t)

    results: dict[str, Any] = {}

    for strat in sorted(strategies):
        results[strat] = {}
        for split in ["dev", "test", "all"]:
            group_traces = grouped.get((strat, split), [])
            n = len(group_traces)
            if n == 0:
                continue

            h1 = sum(1 for t in group_traces if t.get("hit_at_1"))
            h3 = sum(1 for t in group_traces if t.get("hit_at_3"))

            results[strat][split] = {
                "total": n,
                "hit_at_1_count": h1,
                "hit_at_1_ratio": f"{h1}/{n}",
                "hit_at_1_rate": round(h1 / n, 4),
                "hit_at_1_pct": f"{(h1 / n) * 100:.1f}%",
                "hit_at_3_count": h3,
                "hit_at_3_ratio": f"{h3}/{n}",
                "hit_at_3_rate": round(h3 / n, 4),
                "hit_at_3_pct": f"{(h3 / n) * 100:.1f}%",
            }

    return results
