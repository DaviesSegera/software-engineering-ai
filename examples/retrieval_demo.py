"""Module 4 lexical retrieval over invented passages, not a real manual.

Jaccard word overlap is transparent but weak: no stemming, embeddings,
synonym handling or learned relevance. Never use these passages as
instructions for actual equipment.
"""
import re

PASSAGES = {
    "manual_motor_v1_p1": "Motor energy uses interval average power in watts.",
    "manual_motor_v1_p2": "For simulated motor overheating, inspect ventilation.",
    "manual_network_v1_p1": "For network timeout, inspect the simulated connection.",
}


def tokens(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(query, k=2):
    if not isinstance(query, str) or not query.strip():
        raise ValueError("query must be nonempty text")
    if type(k) is not int or k <= 0:
        raise ValueError("k must be a positive integer")
    query_words = tokens(query)
    scored = []
    for passage_id, passage in PASSAGES.items():
        words = tokens(passage)
        overlap = len(query_words & words)
        if overlap:
            score = overlap / len(query_words | words)
            scored.append((score, passage_id, passage))
    return sorted(scored, key=lambda row: (-row[0], row[1]))[:k]


def read_approved_passage(passage_id, allowed_ids):
    """A local tool boundary. No arbitrary paths or commands are accepted."""
    if passage_id not in allowed_ids or passage_id not in PASSAGES:
        raise PermissionError("document is outside the allowed set")
    return PASSAGES[passage_id]


if __name__ == "__main__":
    for query in ("motor overheating", "network timeout", "thermal blockage"):
        print("Query:", query)
        matches = retrieve(query)
        for score, passage_id, passage in matches:
            print(f"  {score:.3f} {passage_id}: {passage}")
        if not matches:
            print("  No lexical match; this does not prove no relevant passage exists.")
