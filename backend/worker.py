import os
import json
import httpx
from typing import Any
from .task_queue import queue
from .brain import route_command
from .db import add_agent_report, audit_events
from .tools import classify_command, execute_internal_tool

OPENAI_URL = "https://api.openai.com/v1/responses"

def _model() -> str:
    return os.getenv("DIMRI_WORKER_MODEL", "gpt-5.6-luna")

def worker_status() -> dict[str, Any]:
    return {
        "enabled": bool(os.getenv("OPENAI_API_KEY")),
        "provider": "openai_responses",
        "model": _model(),
        "mode": "live" if os.getenv("OPENAI_API_KEY") else "awaiting_provider_key",
        "execution_policy": "permissioned_tools_founder_gate",
    }

async def execute_task(task: dict[str, Any]) -> dict[str, Any]:
    key = os.getenv("OPENAI_API_KEY")
    tool_id = classify_command(task["command"])

    if tool_id and tool_id in {"youtube.create_draft", "digital_product.create_draft"}:
        result = await execute_internal_tool(tool_id, {
            "topic": task["command"],
            "title": task["command"][:100],
            "script": "",
            "visual_prompt": "",
        })
        return {"executed": result.get("executed", False), "status": result.get("status"), "tool": tool_id, "tool_result": result}

    if tool_id == "ghost.review_claims":
        return {"executed": False, "status": "awaiting_structured_claims", "tool": tool_id,
                "reason": "Ghost Mode requires structured claims and evidence fields before review."}

    if tool_id and tool_id in {"youtube.publish", "meta.publish", "commerce.publish"}:
        return {"executed": False, "status": "blocked", "tool": tool_id,
                "reason": "External publishing remains disabled until verified OAuth/API integration and founder-approved execution are configured."}

    if not key:
        return {"executed": False, "status": "awaiting_provider_key", "reason": "OPENAI_API_KEY is not configured on the server."}

    routes = route_command(task["command"])
    system = (
        "You are the DIMRI AI worker coordinator. Produce a concise execution plan/result. "
        "Do not claim external actions were completed. Use only permissioned tools when explicitly available. "
        "Never publish, send messages, spend money, deploy production, or modify external systems. "
        "Return summary, next_steps, risks, requires_approval, and suggested_agent_report."
    )
    payload = {"model": _model(), "input": [
        {"role": "system", "content": system},
        {"role": "user", "content": json.dumps({
            "task_id": task["id"], "command": task["command"], "priority": task["priority"],
            "assigned_agent": task.get("assigned_agent"), "routes": routes
        })}
    ]}
    headers = {"Authorization": f"Bearer {key}", "Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=90) as client:
        response = await client.post(OPENAI_URL, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
    return {"executed": True, "status": "completed", "provider": "openai_responses",
            "model": _model(), "summary": data.get("output_text", ""),
            "response_id": data.get("id"), "requires_approval": True, "routes": routes}

async def run_worker_once(limit: int = 5) -> dict[str, Any]:
    approved = queue.list("approved")
    queued = queue.list("queued")
    tasks = (approved + queued)[:max(1, min(limit, 20))]
    results = []
    for task in tasks:
        queue.update(task["id"], "in_progress", None)
        try:
            result = await execute_task(task)
            if result.get("status") == "blocked":
                final_status = "awaiting_execution"
            elif result.get("status") in {"awaiting_provider_key", "awaiting_structured_claims"}:
                final_status = "awaiting_execution"
            else:
                final_status = "completed" if result.get("executed") else "awaiting_execution"
            queue.update(task["id"], final_status, json.dumps(result))
            if result.get("executed"):
                agent_id = task.get("assigned_agent") or "ceo"
                add_agent_report(agent_id, "task_execution", json.dumps(result)[:8000], "completed")
            results.append({"task_id": task["id"], "result": result})
        except Exception as exc:
            error_result = {"executed": False, "status": "failed", "error": str(exc)}
            queue.update(task["id"], "failed", json.dumps(error_result))
            add_agent_report(task.get("assigned_agent") or "ceo", "task_execution", f"Task {task['id']} failed: {exc}", "failed")
            results.append({"task_id": task["id"], "result": error_result})
    return {"processed": len(results), "results": results, "worker": worker_status(),
            "recent_audit_count": len(audit_events(20))}
