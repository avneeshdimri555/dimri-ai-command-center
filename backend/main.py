from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .brain import memory, create_workflow, route_command

app = FastAPI(title="DIMRI AI Company OS", version="0.3.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

class Command(BaseModel):
    command: str
    priority: str = "normal"

class Workflow(BaseModel):
    name: str
    objective: str
    department: str | None = None

@app.get("/api/health")
def health() -> dict[str, Any]:
    return {"ok": True, "service": "dimri-ai-company-os", "time": datetime.now(timezone.utc).isoformat()}

@app.get("/api/brain")
def brain() -> dict[str, Any]:
    return {"name":"DIMRI Company Brain","state":"foundation","memory":memory.context(),"routing_capabilities":8}

@app.post("/api/brain/route")
def brain_route(command: Command) -> dict[str, Any]:
    return {"accepted":True,"command":command.command,"priority":command.priority,"routes":route_command(command.command)}

@app.post("/api/workflows")
def create_company_workflow(workflow: Workflow) -> dict[str, Any]:
    result = create_workflow(workflow.objective)
    result["name"] = workflow.name
    result["department"] = workflow.department
    return result

@app.post("/api/commands")
def create_command(command: Command) -> dict[str, Any]:
    result = create_workflow(command.command, command.priority)
    return {"accepted": True, "status": "queued", "workflow": result}

@app.post("/api/memory")
def remember(kind: str, content: str, source: str = "founder") -> dict[str, Any]:
    return memory.remember(kind, content, source)

@app.get("/api/memory")
def get_memory() -> dict[str, Any]:
    return memory.context()

@app.get("/api/company")
def company() -> dict[str, Any]:
    return {
        "name":"DIMRI AI","mode":"Founder Controlled","departments":8,
        "planned_agents":90,"products_services":50,
        "principles":{"ghost_mode_real_info_first":True,"source_verification":True,
        "founder_approval_for_consequential_actions":True,"no_impersonation":True,"no_bulk_spam":True}
    }
