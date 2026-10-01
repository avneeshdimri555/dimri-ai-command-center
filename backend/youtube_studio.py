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
          updated_at TEXT NOT NULL, video_id TEXT, video_url TEXT,
          published_at TEXT, publish_error TEXT
        );
        CREATE TABLE IF NOT EXISTS youtube_channel_automation (
          channel_id TEXT PRIMARY KEY, content_brief TEXT NOT NULL,
          shorts_per_day INTEGER NOT NULL DEFAULT 1,
          long_videos_per_week INTEGER NOT NULL DEFAULT 1,
          mode TEXT NOT NULL DEFAULT 'approval',
          enabled INTEGER NOT NULL DEFAULT 0,
          updated_at TEXT NOT NULL,
          FOREIGN KEY(channel_id) REFERENCES youtube_channels(channel_id) ON DELETE CASCADE
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

def _ensure_content_columns():
    with connect() as conn:
        cols={row["name"] for row in conn.execute("PRAGMA table_info(youtube_content)").fetchall()}
        for name, sql_type in [("video_id","TEXT"),("video_url","TEXT"),("published_at","TEXT"),("publish_error","TEXT")]:
            if name not in cols:
                conn.execute("ALTER TABLE youtube_content ADD COLUMN " + name + " " + sql_type)

def mark_published(content_id, video_id, video_url):
    with connect() as conn:
        conn.execute("UPDATE youtube_content SET status='published', video_id=?, video_url=?, published_at=?, publish_error=NULL, updated_at=? WHERE id=?",
                     (video_id, video_url, _now(), _now(), content_id))
        row=conn.execute("SELECT * FROM youtube_content WHERE id=?",(content_id,)).fetchone()
    return dict(row) if row else None

def mark_publish_error(content_id, error):
    with connect() as conn: conn.execute("UPDATE youtube_content SET publish_error=?, updated_at=? WHERE id=?",(str(error)[:2000],_now(),content_id))
    with connect() as conn: row=conn.execute("SELECT * FROM youtube_content WHERE id=?",(content_id,)).fetchone()
    return dict(row) if row else None

init_youtube_tables()
_ensure_content_columns()


def get_channel_automation(channel_id):
    with connect() as conn:
        row=conn.execute("SELECT * FROM youtube_channel_automation WHERE channel_id=?",(channel_id,)).fetchone()
    if not row: return None
    item=dict(row);item["enabled"]=bool(item["enabled"]);return item


def save_channel_automation(channel_id, content_brief, shorts_per_day=1,
                            long_videos_per_week=1, mode="approval", enabled=False):
    channel=next((x for x in list_channels() if x["channel_id"]==channel_id),None)
    if not channel:return None
    timestamp=_now()
    with connect() as conn:
        conn.execute(
            "INSERT INTO youtube_channel_automation (channel_id,content_brief,shorts_per_day,long_videos_per_week,mode,enabled,updated_at) VALUES (?,?,?,?,?,?,?) "
            "ON CONFLICT(channel_id) DO UPDATE SET content_brief=excluded.content_brief,shorts_per_day=excluded.shorts_per_day,long_videos_per_week=excluded.long_videos_per_week,mode=excluded.mode,enabled=excluded.enabled,updated_at=excluded.updated_at",
            (channel_id,content_brief.strip(),shorts_per_day,long_videos_per_week,mode,int(enabled),timestamp))
        conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)",
                     (str(uuid4()),"youtube_automation_saved","Founder",channel_id,timestamp))
    return get_channel_automation(channel_id)
