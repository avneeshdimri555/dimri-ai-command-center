"""DIMRI agent runtime boundary.

This module is intentionally credential-free. Set OPENAI_API_KEY only in the runtime environment.
The OpenAI Agents SDK supports tools, handoffs, guardrails and human review; DIMRI keeps
consequential marketplace publishing behind its own approval layer.
"""
import os
from typing import Any

def runtime_status() -> dict[str, Any]:
    return {
        "provider": "OpenAI Agents SDK",
        "configured": bool(os.getenv("OPENAI_API_KEY")),
        "execution_mode": "sdk-ready",
        "approval_layer": "DIMRI founder gate",
        "external_agent_webhook_configured": bool(os.getenv("DIGITAL_PRODUCT_AGENT_WEBHOOK")),
    }
