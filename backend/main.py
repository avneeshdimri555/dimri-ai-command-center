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
    {"id":"after-sales","name":"After-Sales Service Agent","department":"After-Sales & Retention","status":"ready"},
    {"id":"retention","name":"Retention Agent","department":"After-Sales & Retention","status":"ready"},
    {"id":"renewal","name":"Renewal Agent","department":"After-Sales & Retention","status":"ready"},
    {"id":"feedback","name":"Customer Feedback Agent","department":"After-Sales & Retention","status":"ready"},
    {"id":"warranty","name":"Warranty & Support Agent","department":"After-Sales & Retention","status":"ready"},
    {"id":"finance","name":"Finance Head Agent","department":"Finance","status":"ready"},
    {"id":"accounting","name":"Accounting Agent","department":"Finance","status":"ready"},
    {"id":"bookkeeping","name":"Bookkeeping Agent","department":"Finance","status":"ready"},
    {"id":"invoicing","name":"Invoicing Agent","department":"Finance","status":"ready"},
    {"id":"payments","name":"Payment Tracking Agent","department":"Finance","status":"ready"},
    {"id":"cashflow","name":"Cashflow Agent","department":"Finance","status":"ready"},
    {"id":"profit","name":"Profit & Loss Agent","department":"Finance","status":"ready"},
    {"id":"budget","name":"Budget Agent","department":"Finance","status":"ready"},
    {"id":"finance-reporting","name":"Financial Reporting Agent","department":"Finance","status":"ready"},
    {"id":"pricing","name":"Pricing Agent","department":"Finance","status":"ready"},
    {"id":"cost","name":"Cost Optimization Agent","department":"Finance","status":"ready"},
    {"id":"tax-support","name":"Tax Preparation Support Agent","department":"Finance","status":"ready"},
    {"id":"finance-audit","name":"Finance Audit Agent","department":"Finance","status":"ready"},
    {"id":"ops-head","name":"Operations Head Agent","department":"Operations","status":"ready"},
    {"id":"workflow","name":"Workflow Coordinator Agent","department":"Operations","status":"ready"},
    {"id":"project-ops","name":"Project Operations Agent","department":"Operations","status":"ready"},
    {"id":"scheduling","name":"Scheduling Agent","department":"Operations","status":"ready"},
    {"id":"sop","name":"SOP Manager Agent","department":"Operations","status":"ready"},
    {"id":"knowledge","name":"Knowledge Operations Agent","department":"Operations","status":"ready"},
    {"id":"automation-monitor","name":"Automation Monitor Agent","department":"Operations","status":"ready"},
    {"id":"incident","name":"Incident Response Agent","department":"Operations","status":"ready"},
    {"id":"vendor","name":"Vendor Operations Agent","department":"Operations","status":"ready"},
    {"id":"procurement","name":"Procurement Agent","department":"Operations","status":"ready"},
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

@app.post("/api/brain/route")
def route_command(command: Command) -> dict[str, Any]:
    text = command.command.lower()
    routes = []
    if any(k in text for k in ["video", "youtube", "instagram", "reel", "content", "ghost"]):
        routes.append({"department":"Content & Media","agents":["Ghost Mode Agent","Trend Research Agent","Script Agent","Video Agent"]})
    if any(k in text for k in ["customer", "client", "lead", "business", "sales", "outreach"]):
        routes.append({"department":"Sales & Business","agents":["Lead Research Agent","Outreach Agent","Conversation Agent","Proposal Agent"]})
    if any(k in text for k in ["website", "app", "software", "build", "product"]):
        routes.append({"department":"Product & Development","agents":["Product Manager Agent","Software Builder Agent","QA Agent"]})
    if any(k in text for k in ["marketing", "seo", "campaign", "brand"]):
        routes.append({"department":"Marketing & Growth","agents":["Marketing Head Agent","SEO Agent","Analytics Agent"]})
    if any(k in text for k in ["after sales", "after-sales", "renewal", "retention", "feedback", "warranty"]):
        routes.append({"department":"After-Sales & Retention","agents":["After-Sales Service Agent","Customer Feedback Agent","Retention Agent","Renewal Agent"]})
    if any(k in text for k in ["finance", "revenue", "expense", "invoice", "payment", "cashflow", "profit", "budget", "tax", "pricing"]):
        routes.append({"department":"Finance","agents":["Finance Head Agent","Accounting Agent","Invoicing Agent","Cashflow Agent","Financial Reporting Agent"]})
    if any(k in text for k in ["operations", "ops", "workflow", "sop", "schedule", "vendor", "procurement", "incident", "automation"]):
        routes.append({"department":"Operations","agents":["Operations Head Agent","Workflow Coordinator Agent","SOP Manager Agent","Automation Monitor Agent"]})
    if any(k in text for k in ["support", "billing", "delivery", "onboard"]):
        routes.append({"department":"Operations & Support","agents":["Customer Success Agent","Support Agent","Delivery Coordinator"]})
    if not routes:
        routes.append({"department":"Executive","agents":["DIMRI CEO"]})
    return {"accepted":True,"command":command.command,"priority":command.priority,"status":"routed","routes":routes}

@app.get("/api/brain")
def brain() -> dict[str, Any]:
    return {
        "name":"DIMRI Company Brain",
        "state":"foundation",
        "layers":["Founder Intent","DIMRI CEO","Department Heads","Specialist Agents","Tools","Memory","Audit"],
        "principles":["delegate by capability","verify evidence","permission consequential actions","report outcomes"],
    }

@app.get("/api/company")
def company() -> dict[str, Any]:
    return {"name":"DIMRI AI","mode":"Founder Controlled","departments":5,"planned_agents":58,"products_services":50,"principles":{"ghost_mode_real_info_first":True,"source_verification":True,"founder_approval_for_consequential_actions":True,"no_impersonation":True,"no_bulk_spam":True}}
