"""Evidence-first Ghost Mode review helpers.

This module performs deterministic completeness/risk checks only. It does not
browse sources, validate URLs, or independently verify factual claims.
"""
from __future__ import annotations

import re
from typing import Any

RISK_PATTERNS = {
    "numeric_claim": re.compile(r"(?<!\\w)(?:\\d[\\d,.%]*|\\$\\s?\\d+|₹\\s?\\d+)(?!\\w)", re.I),
    "absolute_claim": re.compile(r"\\b(always|never|all|none|everyone|nobody|guaranteed|proven|100%)\\b", re.I),
    "health_or_finance": re.compile(r"\\b(cure|treat|diagnose|risk-free|guaranteed returns|investment advice)\\b", re.I),
}


def review_claims(claims: list[dict[str, Any]]) -> dict[str, Any]:
    """Check whether claims carry evidence metadata; never infer verification."""
    reviewed = []
    for index, raw in enumerate(claims, start=1):
        claim = str(raw.get("claim") or "").strip()
        source = str(raw.get("source_name") or "").strip()
        url = str(raw.get("source_url") or "").strip()
        evidence = str(raw.get("evidence_note") or "").strip()
        flags = [name for name, pattern in RISK_PATTERNS.items() if pattern.search(claim)]
        missing = []
        if not claim:
            missing.append("claim_text")
        if not source:
            missing.append("source_name")
        if not url:
            missing.append("source_url")
        if not evidence:
            missing.append("evidence_note")
        reviewed.append({
            "index": index,
            "claim": claim,
            "risk_flags": flags,
            "missing_evidence_fields": missing,
            "evidence_attached": bool(source and url and evidence),
            "verification_status": "not_independently_verified",
            "review_status": "needs_evidence" if missing else "human_verification_required",
        })

    incomplete = sum(bool(item["missing_evidence_fields"]) for item in reviewed)
    return {
        "claim_count": len(reviewed),
        "claims": reviewed,
        "evidence_incomplete_count": incomplete,
        "verification_status": "not_independently_verified",
        "content_gate": "blocked_missing_evidence" if incomplete else "ready_for_human_fact_check",
        "publish_status": "founder_approval_required",
        "disclaimer": (
            "Ghost Mode checks evidence-field completeness and risk patterns only. "
            "It does not open URLs, confirm source reliability, or prove claims true. "
            "A human must compare each claim with its cited evidence before approval."
        ),
    }


def status() -> dict[str, Any]:
    return {
        "mode": "evidence_first",
        "checks": [
            "claim_evidence_completeness",
            "numeric_and_absolute_language_flags",
            "human_fact_check_gate",
            "founder_approval_gate",
        ],
        "live_research_connected": False,
        "automatic_fact_verification": False,
        "publishing_enabled": False,
    }
