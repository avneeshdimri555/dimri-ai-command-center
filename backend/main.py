from datetime import datetime, timezone
from typing import Any
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="DIMRI AI Company OS", version="0.2.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

AGENTS = [
    {"id":"ceo","name":"DIMRI CEO","department":"Executive","status":"ready"},
    {"id":"ghost","name":"Ghost Mode Agent","department":"Content & Media","status":"ready"},
    {"id":"research","name":"Trend Research Agent","department":"Content & Media","status":"ready"},
    {"id":"marketing","name":"Marketing Head Agent","department":"Marketing & Growth","status":"ready"},
    {"id":"lead-research","name":"Lead Research Agent","department":"Sales & Business","status":"ready"},
    {"id":"outreach","name":"Outreach Agent","department":"Sales & Business","status":"ready"},
    {"id":"product","name":"Product Manager Agent","department":"Product & Development","status":"ready"},
    {"id":"builder","name":"Software Builder Agent","department":"Product & Development","status":"ready"},
    {"id":"qa","name":"QA Agent","department":"Product & Development","status":"ready"},
    {"id":"support","name":"Customer Success Agent","department":"Operations & Support","status":"ready"},
    {"id":"finance","name":"Finance Agent","department":"Operations & Support","status":"ready"},
    {"id":"security","name":"Security Agent","department":"Operations & Support","status":"ready"},
]

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

@app.get("/api/agents")
def agents() -> dict[str, Any]:
    return {"count": len(AGENTS), "agents": AGENTS}

@app.post("/api/commands")
def create_command(command: Command) -> dict[str, Any]:
    return {"accepted": True, "id": f"cmd-{int(datetime.now(timezone.utc).timestamp())}", "command": command.command, "priority": command.priority, "next": "DIMRI CEO", "status": "queued", "note": "Execution connectors are intentionally not enabled in this foundation build."}

@app.post("/api/workflows")
def create_workflow(workflow: Workflow) -> dict[str, Any]:
    return {"accepted": True, "workflow": workflow.model_dump(), "status": "queued", "created_at": datetime.now(timezone.utc).isoformat()}

@app.get("/api/company")
def company() -> dict[str, Any]:
    return {"name":"DIMRI AI","mode":"Founder Controlled","departments":5,"planned_agents":58,"products_services":50,"principles":{"ghost_mode_real_info_first":True,"source_verification":True,"founder_approval_for_consequential_actions":True,"no_impersonation":True,"no_bulk_spam":True}}
