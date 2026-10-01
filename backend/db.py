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
