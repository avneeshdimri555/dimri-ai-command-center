"""Facebook Page registry groundwork.

Stores non-secret Page metadata only. This does not authenticate Meta accounts,
validate Page ownership, or enable publishing/insights. OAuth and Meta review
must be implemented before protected Graph API actions are enabled.
"""
from __future__ import annotations

from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

from .db import connect


def init_facebook_table() -> None:
    with connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS facebook_pages (
                id TEXT PRIMARY KEY,
                page_name TEXT NOT NULL,
                page_id TEXT NOT NULL UNIQUE,
                page_url TEXT NOT NULL DEFAULT '',
                connection_state TEXT NOT NULL DEFAULT 'manual_registry',
                created_at TEXT NOT NULL
            )
        """)


def list_pages() -> list[dict[str, Any]]:
    with connect() as conn:
        rows = conn.execute("SELECT * FROM facebook_pages ORDER BY created_at DESC")
        return [dict(row) for row in rows]


def add_page(page_name: str, page_id: str, page_url: str = "") -> dict[str, Any]:
    page_name = page_name.strip()
    page_id = page_id.strip()
    page_url = page_url.strip()
    if not page_name or not page_id:
        raise ValueError("Page name and Page ID are required")
    item = {
        "id": str(uuid4()),
        "page_name": page_name,
        "page_id": page_id,
        "page_url": page_url,
        "connection_state": "manual_registry",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    with connect() as conn:
        existing = conn.execute("SELECT * FROM facebook_pages WHERE page_id=?", (page_id,)).fetchone()
        if existing:
            raise ValueError("This Facebook Page ID is already registered")
        conn.execute(
            "INSERT INTO facebook_pages(id,page_name,page_id,page_url,connection_state,created_at) VALUES(:id,:page_name,:page_id,:page_url,:connection_state,:created_at)",
            item,
        )
    return item


init_facebook_table()
