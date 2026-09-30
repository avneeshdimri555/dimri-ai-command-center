from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .brain import memory, create_workflow, route_command
from .task_queue import queue
from .db import audit_events

app = FastAPI(title="DIMRI AI Company OS", version="0.4.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Command(BaseModel):
    command: str
    priority: str = "normal"

class Workflow(BaseModel):
    name: str
    objective: str
    department: str | None = None

class TaskUpdate(BaseModel):
    status: str
    result: str | None = None

@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "dimri-ai-company-os", "version":"0.4.0", "time": datetime.now(timezone.utc).isoformat()}

@app.get("/api/brain")
def brain() -> dict[str, Any]:
    return {"name":"DIMRI Company Brain","state":"persistent-memory","memory":memory.context(),"routing_capabilities":8}

@app.post("/api/brain/route")
def brain_route(command: Command) -> dict[str, Any]:
    return {"accepted":True,"command":command.command,"priority":command.priority,"routes":route_command(command.command)}

@app.post("/api/workflows")
def create_company_workflow(workflow: Workflow) -> dict[str, Any]:
    result = create_workflow(workflow.objective)
    result["name"] = workflow.name
    result["department"] = workflow.department
    task = queue.enqueue(workflow.objective, "normal", result["routes"][0]["agent"] if result["routes"] else "ceo")
    result["task"] = task
    return result

@app.post("/api/commands")
def create_command(command: Command) -> dict[str, Any]:
    result = create_workflow(command.command, command.priority)
    agent = result["routes"][0]["agent"] if result["routes"] else "ceo"
    task = queue.enqueue(command.command, command.priority, agent)
    return {"accepted": True, "status": "queued", "workflow": result, "task": task}

@app.get("/api/tasks")
def tasks(status: str | None = None) -> dict[str, Any]:
    return {"tasks": queue.list(status), "count": len(queue.list(status))}

@app.patch("/api/tasks/{task_id}")
def task_update(task_id: str, update: TaskUpdate) -> dict[str, Any]:
    task = queue.update(task_id, update.status, update.result)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@app.post("/api/memory")
def remember(kind: str, content: str, source: str = "founder") -> dict[str, Any]:
    return memory.remember(kind, content, source)

@app.get("/api/memory")
def get_memory() -> dict[str, Any]:
    return memory.context()

@app.get("/api/audit")
def audit(limit: int = 50) -> dict[str, Any]:
    return {"events": audit_events(limit)}

@app.get("/api/company")
def company() -> dict[str, Any]:
    return {"name":"DIMRI AI","mode":"Founder Controlled","departments":8,"planned_agents":90,"products_services":50,
        "platforms":["web","mobile","telegram"],
        "state":{"persistent_memory":True,"durable_task_queue":True,"real_agent_execution":False},
        "principles":{"ghost_mode_real_info_first":True,"source_verification":True,"founder_approval_for_consequential_actions":True,"no_impersonation":True,"no_bulk_spam":True}}
