"""YouTube channel registry and content workspace; no external account access until OAuth is configured."""
from uuid import uuid4
from datetime import datetime, timezone
from .db import connect

def _now():
    return datetime.now(timezone.utc).isoformat()

def init_youtube_tables():
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS youtube_channels (
          channel_id TEXT PRIMARY KEY, name TEXT NOT NULL, handle TEXT,
          channel_url TEXT, connection_state TEXT NOT NULL DEFAULT 'manual',
          created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS youtube_content (
          id TEXT PRIMARY KEY, channel_id TEXT, content_type TEXT NOT NULL,
          topic TEXT NOT NULL, title TEXT NOT NULL, description TEXT NOT NULL,
          script TEXT NOT NULL, visual_prompt TEXT NOT NULL,
          status TEXT NOT NULL DEFAULT 'draft', created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        );
        """)

def list_channels():
    with connect() as conn:
        rows=conn.execute("SELECT * FROM youtube_channels ORDER BY created_at DESC").fetchall()
    return [dict(r) for r in rows]

def add_channel(name, handle="", channel_url=""):
    name=(name or "").strip()
    if not name:
        raise ValueError("Channel name is required")
    item={"channel_id":"manual-"+uuid4().hex[:12],"name":name,
          "handle":(handle or "").strip(),"channel_url":(channel_url or "").strip(),
          "connection_state":"manual","created_at":_now()}
    with connect() as conn:
        conn.execute("INSERT INTO youtube_channels VALUES (:channel_id,:name,:handle,:channel_url,:connection_state,:created_at)",item)
    return item

def list_content():
    with connect() as conn:
        rows=conn.execute("SELECT * FROM youtube_content ORDER BY created_at DESC").fetchall()
    return [dict(r) for r in rows]

def create_content(channel_id, content_type, topic, title, description="", script="", visual_prompt=""):
    topic=(topic or "").strip()
    title=(title or "").strip()
    if not topic or not title:
        raise ValueError("Topic and title are required")
    item={"id":"yt-"+uuid4().hex[:12],"channel_id":channel_id or None,
          "content_type":content_type or "short","topic":topic,"title":title,
          "description":description or "","script":script or "",
          "visual_prompt":visual_prompt or "","status":"draft",
          "created_at":_now(),"updated_at":_now()}
    with connect() as conn:
        conn.execute("INSERT INTO youtube_content VALUES (:id,:channel_id,:content_type,:topic,:title,:description,:script,:visual_prompt,:status,:created_at,:updated_at)",item)
    return item

def update_content(content_id, status):
    if status not in {"draft","ready_for_review","approved","scheduled","published"}:
        raise ValueError("Invalid content status")
    with connect() as conn:
        cur=conn.execute("UPDATE youtube_content SET status=?,updated_at=? WHERE id=?",(status,_now(),content_id))
        if not cur.rowcount:
            return None
        row=conn.execute("SELECT * FROM youtube_content WHERE id=?",(content_id,)).fetchone()
    return dict(row)

init_youtube_tables()
