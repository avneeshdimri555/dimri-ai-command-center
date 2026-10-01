import os
import json
import httpx
from typing import Any
from .task_queue import queue
from .brain import route_command
from .db import add_agent_report, audit_events

OPENAI_URL = "https://api.openai.com/v1/responses"

def _model() -> str:
    return os.getenv("DIMRI_WORKER_MODEL", "gpt-5.6-luna")

def worker_status() -> dict[str, Any]:
    return {
        "enabled": bool(os.getenv("OPENAI_API_KEY")),
        "provider": "openai_responses",
        "model": _model(),
        "mode": "live" if os.getenv("OPENAI_API_KEY") else "awaiting_provider_key",
        "execution_policy": "planning_only_no_external_side_effects",
    }

async def execute_task(task: dict[str, Any]) -> dict[str, Any]:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        return {
            "executed": False,
            "status": "awaiting_provider_key",
            "reason": "OPENAI_API_KEY is not configured on the server.",
        }

    routes = route_command(task["command"])
    system = (
        "You are the DIMRI AI worker coordinator. Produce a concise execution plan/result. "
        "Do not claim external actions were completed. Do not publish, send messages, spend money, "
        "deploy production, or modify external systems. Return summary, next_steps, risks, "
        "requires_approval, and suggested_agent_report."
    )
    payload = {
        "model": _model(),
        "input": [
            {"role": "system", "content": system},
            {
                "role": "user",
                "content": json.dumps({
                    "task_id": task["id"],
                    "command": task["command"],
                    "priority": task["priority"],
                    "assigned_agent": task.get("assigned_agent"),
                    "routes": routes,
                }),
            },
        ],
    }
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(OPENAI_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

    summary = data.get("output_text", "")
    return {
        "executed": True,
        "status": "completed",
        "provider": "openai_responses",
        "model": _model(),
        "summary": summary,
        "response_id": data.get("id"),
        "requires_approval": True,
        "routes": routes,
    }

async def run_worker_once(limit: int = 5) -> dict[str, Any]:
    tasks = queue.list("approved")[:max(1, min(limit, 20))]
    results = []

    for task in tasks:
        queue.update(task["id"], "in_progress", None)
        try:
            result = await execute_task(task)
            final_status = "completed" if result["executed"] else "awaiting_execution"
            queue.update(task["id"], final_status, json.dumps(result))

            if result["executed"]:
                agent_id = task.get("assigned_agent") or "ceo"
                summary = result.get("summary") or "Worker completed the task without a textual summary."
                add_agent_report(agent_id, "task_execution", summary, "completed")

            results.append({"task_id": task["id"], "result": result})
        except Exception as exc:
            error_result = {"executed": False, "status": "failed", "error": str(exc)}
            queue.update(task["id"], "failed", json.dumps(error_result))
            add_agent_report(
                task.get("assigned_agent") or "ceo",
                "task_execution",
                f"Task {task['id']} failed: {exc}",
                "failed",
            )
            results.append({"task_id": task["id"], "result": error_result})

    return {
        "processed": len(results),
        "results": results,
        "worker": worker_status(),
        "recent_audit_count": len(audit_events(20)),
    }
