from __future__ import annotations
from typing import Any, Callable
from .youtube_studio import create_content
from .digital_products import create_product
from .ghost_mode import review_claims

TOOL_REGISTRY: dict[str, dict[str, Any]] = {
    "youtube.create_draft": {
        "description": "Create a YouTube content draft in the local workspace.",
        "risk": "internal_write",
        "external": False,
    },
    "digital_product.create_draft": {
        "description": "Create a digital product draft in the local workspace.",
        "risk": "internal_write",
        "external": False,
    },
    "ghost.review_claims": {
        "description": "Run deterministic Ghost Mode claim QA on supplied claims.",
        "risk": "internal_read",
        "external": False,
    },
    "youtube.publish": {
        "description": "Publish content to YouTube.",
        "risk": "external_publish",
        "external": True,
    },
    "meta.publish": {
        "description": "Publish content through Meta platforms.",
        "risk": "external_publish",
        "external": True,
    },
    "commerce.publish": {
        "description": "Publish or sell a digital product on an external marketplace.",
        "risk": "external_publish",
        "external": True,
    },
}

def list_tools() -> list[dict[str, Any]]:
    return [{"id": tool_id, **spec} for tool_id, spec in TOOL_REGISTRY.items()]

def classify_command(command: str) -> str | None:
    text = command.lower()
    if "ghost" in text or "claim" in text and ("source" in text or "verify" in text):
        return "ghost.review_claims"
    if ("youtube" in text or "short" in text or "video" in text) and any(x in text for x in ("create", "draft", "script", "idea")):
        return "youtube.create_draft"
    if ("digital product" in text or "gumroad" in text or "sticker" in text) and any(x in text for x in ("create", "draft", "make")):
        return "digital_product.create_draft"
    if "youtube" in text and any(x in text for x in ("publish", "post", "upload")):
        return "youtube.publish"
    if any(x in text for x in ("facebook", "instagram", "meta")) and any(x in text for x in ("publish", "post", "upload")):
        return "meta.publish"
    if any(x in text for x in ("gumroad", "marketplace", "sell")) and any(x in text for x in ("publish", "post", "upload", "sell")):
        return "commerce.publish"
    return None

async def execute_internal_tool(tool_id: str, args: dict[str, Any]) -> dict[str, Any]:
    if tool_id not in TOOL_REGISTRY:
        raise ValueError("Unknown tool")
    spec = TOOL_REGISTRY[tool_id]
    if spec["external"]:
        return {
            "executed": False,
            "status": "blocked",
            "reason": "External side effect requires a verified integration and founder approval.",
            "tool": tool_id,
        }

    if tool_id == "youtube.create_draft":
        return {"executed": True, "status": "created", "tool": tool_id,
                "result": create_content(
                    channel_id=args.get("channel_id"),
                    content_type=args.get("content_type", "short"),
                    topic=args.get("topic", "DIMRI AI generated topic"),
                    title=args.get("title", "Untitled draft"),
                    description=args.get("description", ""),
                    script=args.get("script", ""),
                    visual_prompt=args.get("visual_prompt", ""),
                )}

    if tool_id == "digital_product.create_draft":
        return {"executed": True, "status": "created", "tool": tool_id,
                "result": create_product(
                    title=args.get("title", "Untitled product"),
                    product_type=args.get("product_type", "digital-product"),
                    description=args.get("description", ""),
                    price=args.get("price"),
                    currency=args.get("currency", "USD"),
                    asset_path=args.get("asset_path"),
                    marketplaces=args.get("marketplaces", "gumroad"),
                )}

    if tool_id == "ghost.review_claims":
        claims = args.get("claims", [])
        return {"executed": True, "status": "reviewed", "tool": tool_id,
                "result": review_claims(claims)}

    raise ValueError("Tool implementation missing")
