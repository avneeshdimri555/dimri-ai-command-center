import sqlite3
from pathlib import Path
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

DB_PATH = Path(__file__).resolve().parent / "dimri_company.db"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def connect() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with connect() as conn:
        conn.executescript("""
        CREATE TABLE IF NOT EXISTS memory (
            id TEXT PRIMARY KEY, kind TEXT NOT NULL, content TEXT NOT NULL,
            source TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS decisions (
            id TEXT PRIMARY KEY, decision TEXT NOT NULL, rationale TEXT,
            created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id TEXT PRIMARY KEY, command TEXT NOT NULL, priority TEXT NOT NULL,
            status TEXT NOT NULL, assigned_agent TEXT, created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL, result TEXT
        );
        CREATE TABLE IF NOT EXISTS audit_log (
            id TEXT PRIMARY KEY, event TEXT NOT NULL, actor TEXT NOT NULL,
            details TEXT, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS agent_reports (
            id TEXT PRIMARY KEY, agent_id TEXT NOT NULL, report_type TEXT NOT NULL,
            summary TEXT NOT NULL, status TEXT NOT NULL, created_at TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS approvals (
            id TEXT PRIMARY KEY, task_id TEXT NOT NULL, action TEXT NOT NULL,
            reason TEXT NOT NULL, status TEXT NOT NULL, decision_note TEXT,
            created_at TEXT NOT NULL, decided_at TEXT
        );
        CREATE TABLE IF NOT EXISTS personas (
            id TEXT PRIMARY KEY, persona_name TEXT NOT NULL,
            gender_presentation TEXT NOT NULL, visual_identity TEXT NOT NULL,
            voice_dna TEXT NOT NULL, content_goal TEXT NOT NULL,
            status TEXT NOT NULL, tags TEXT NOT NULL DEFAULT '[]',
            linked_campaigns TEXT NOT NULL DEFAULT '[]',
            created_at TEXT NOT NULL, updated_at TEXT NOT NULL
        );
        """)


def add_memory(kind: str, content: str, source: str = "system") -> dict[str, Any]:
    item = {"id": str(uuid4()), "kind": kind, "content": content, "source": source, "created_at": now()}
    with connect() as conn:
        conn.execute("INSERT INTO memory VALUES (:id,:kind,:content,:source,:created_at)", item)
    return item


def memory_context() -> dict[str, Any]:
    with connect() as conn:
        knowledge = [dict(r) for r in conn.execute("SELECT * FROM memory ORDER BY created_at DESC LIMIT 50")]
        decisions = [dict(r) for r in conn.execute("SELECT * FROM decisions ORDER BY created_at DESC LIMIT 20")]
    return {"decisions": decisions, "knowledge": knowledge}


def enqueue_task(command: str, priority: str = "normal", assigned_agent: str | None = None) -> dict[str, Any]:
    task = {"id": f"task-{uuid4().hex[:10]}", "command": command, "priority": priority,
            "status": "queued", "assigned_agent": assigned_agent, "created_at": now(), "updated_at": now(), "result": None}
    with connect() as conn:
        conn.execute("INSERT INTO tasks VALUES (:id,:command,:priority,:status,:assigned_agent,:created_at,:updated_at,:result)", task)
        conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)", (str(uuid4()), "task_queued", "DIMRI CEO", task["id"], now()))
    return task


def list_tasks(status: str | None = None) -> list[dict[str, Any]]:
    with connect() as conn:
        if status:
            rows = conn.execute("SELECT * FROM tasks WHERE status=? ORDER BY created_at DESC", (status,))
        else:
            rows = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC LIMIT 100")
        return [dict(r) for r in rows]


def update_task(task_id: str, status: str, result: str | None = None) -> dict[str, Any] | None:
    with connect() as conn:
        conn.execute("UPDATE tasks SET status=?, result=?, updated_at=? WHERE id=?", (status, result, now(), task_id))
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row:
            conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)", (str(uuid4()), "task_status", "DIMRI CEO", f"{task_id}:{status}", now()))
            return dict(row)
    return None


def audit_events(limit: int = 50) -> list[dict[str, Any]]:
    with connect() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM audit_log ORDER BY created_at DESC LIMIT ?", (limit,))]

init_db()


def add_agent_report(agent_id: str, report_type: str, summary: str, status: str = "submitted") -> dict[str, Any]:
    report = {
        "id": f"report-{uuid4().hex[:10]}",
        "agent_id": agent_id,
        "report_type": report_type,
        "summary": summary,
        "status": status,
        "created_at": now(),
    }
    with connect() as conn:
        conn.execute("INSERT INTO agent_reports VALUES (:id,:agent_id,:report_type,:summary,:status,:created_at)", report)
        conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)", (str(uuid4()), "agent_report", agent_id, report["id"], now()))
    return report


def list_agent_reports(agent_id: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    with connect() as conn:
        if agent_id:
            rows = conn.execute("SELECT * FROM agent_reports WHERE agent_id=? ORDER BY created_at DESC LIMIT ?", (agent_id, limit))
        else:
            rows = conn.execute("SELECT * FROM agent_reports ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]


def add_approval(task_id: str, action: str, reason: str) -> dict[str, Any]:
    item = {"id": f"approval-{uuid4().hex[:10]}", "task_id": task_id, "action": action,
            "reason": reason, "status": "pending", "decision_note": None,
            "created_at": now(), "decided_at": None}
    with connect() as conn:
        conn.execute("INSERT INTO approvals VALUES (:id,:task_id,:action,:reason,:status,:decision_note,:created_at,:decided_at)", item)
        conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)", (str(uuid4()), "approval_requested", "DIMRI CEO", item["id"], now()))
    return item

def list_approvals(status: str | None = None, limit: int = 100) -> list[dict[str, Any]]:
    with connect() as conn:
        if status:
            rows = conn.execute("SELECT * FROM approvals WHERE status=? ORDER BY created_at DESC LIMIT ?", (status, limit))
        else:
            rows = conn.execute("SELECT * FROM approvals ORDER BY created_at DESC LIMIT ?", (limit,))
        return [dict(r) for r in rows]

def decide_approval(approval_id: str, status: str, decision_note: str = "") -> dict[str, Any] | None:
    if status not in {"approved", "rejected"}:
        raise ValueError("Approval status must be approved or rejected")
    with connect() as conn:
        conn.execute("UPDATE approvals SET status=?, decision_note=?, decided_at=? WHERE id=? AND status='pending'", (status, decision_note, now(), approval_id))
        row = conn.execute("SELECT * FROM approvals WHERE id=?", (approval_id,)).fetchone()
        if row:
            conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)", (str(uuid4()), "approval_decision", "Founder", f"{approval_id}:{status}", now()))
            return dict(row)
    return None


def list_personas() -> list[dict[str, Any]]:
    import json
    with connect() as conn:
        rows = conn.execute("SELECT * FROM personas ORDER BY updated_at DESC").fetchall()
    result = []
    for row in rows:
        item = dict(row)
        for field in ("tags", "linked_campaigns"):
            try:
                item[field] = json.loads(item.get(field) or "[]")
            except (TypeError, ValueError):
                item[field] = []
        result.append(item)
    return result


def create_persona(persona_name: str, gender_presentation: str = "Androgynous",
                   visual_identity: str = "", voice_dna: str = "",
                   content_goal: str = "", tags: list[str] | None = None,
                   linked_campaigns: list[str] | None = None) -> dict[str, Any]:
    import json
    name = persona_name.strip()
    if not name:
        raise ValueError("Persona name is required")
    timestamp = now()
    item = {
        "id": f"persona-{uuid4().hex[:12]}",
        "persona_name": name,
        "gender_presentation": gender_presentation.strip() or "Androgynous",
        "visual_identity": visual_identity.strip(),
        "voice_dna": voice_dna.strip(),
        "content_goal": content_goal.strip(),
        "status": "draft",
        "tags": json.dumps(tags or [], ensure_ascii=False),
        "linked_campaigns": json.dumps(linked_campaigns or [], ensure_ascii=False),
        "created_at": timestamp,
        "updated_at": timestamp,
    }
    with connect() as conn:
        conn.execute(
            "INSERT INTO personas (id,persona_name,gender_presentation,visual_identity,voice_dna,content_goal,status,tags,linked_campaigns,created_at,updated_at) "
            "VALUES (:id,:persona_name,:gender_presentation,:visual_identity,:voice_dna,:content_goal,:status,:tags,:linked_campaigns,:created_at,:updated_at)",
            item,
        )
        conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)",
                     (str(uuid4()), "persona_created", "Founder", item["id"], timestamp))
    item["tags"] = tags or []
    item["linked_campaigns"] = linked_campaigns or []
    return item


def update_persona(persona_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
    import json
    allowed = {"persona_name", "gender_presentation", "visual_identity", "voice_dna",
               "content_goal", "status", "tags", "linked_campaigns"}
    changes = {k: v for k, v in updates.items() if k in allowed}
    if not changes:
        with connect() as conn:
            row = conn.execute("SELECT * FROM personas WHERE id=?", (persona_id,)).fetchone()
        return dict(row) if row else None
    if "persona_name" in changes:
        changes["persona_name"] = str(changes["persona_name"]).strip()
        if not changes["persona_name"]:
            raise ValueError("Persona name is required")
    for field in ("tags", "linked_campaigns"):
        if field in changes:
            changes[field] = json.dumps(changes[field] or [], ensure_ascii=False)
    changes["updated_at"] = now()
    setters = ", ".join(f"{key}=:{key}" for key in changes)
    changes["id"] = persona_id
    with connect() as conn:
        conn.execute(f"UPDATE personas SET {setters} WHERE id=:id", changes)
        row = conn.execute("SELECT * FROM personas WHERE id=?", (persona_id,)).fetchone()
        if row:
            conn.execute("INSERT INTO audit_log VALUES (?,?,?,?,?)",
                         (str(uuid4()), "persona_updated", "Founder", persona_id, now()))
    if not row:
        return None
    item = dict(row)
    for field in ("tags", "linked_campaigns"):
        try:
            item[field] = json.loads(item.get(field) or "[]")
        except (TypeError, ValueError):
            item[field] = []
    return item
