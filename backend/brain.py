from datetime import datetime, timezone
from typing import Any
from uuid import uuid4
from .db import add_memory, memory_context

class CompanyMemory:
    def remember(self, kind: str, content: str, source: str = "system"):
        return add_memory(kind, content, source)

    def add_decision(self, decision: str, rationale: str = ""):
        from .db import connect
        item = {"id": str(uuid4()), "decision": decision, "rationale": rationale, "created_at": datetime.now(timezone.utc).isoformat()}
        with connect() as conn:
            conn.execute("INSERT INTO decisions VALUES (:id,:decision,:rationale,:created_at)", item)
        return item

    def context(self) -> dict[str, Any]:
        return {"company": {"name":"DIMRI AI", "principles":["real_info_first","founder_controlled","permissioned_actions"]}, **memory_context()}

memory = CompanyMemory()

AGENT_CAPABILITIES = {
    "ghost": ["content", "video", "instagram", "youtube", "ghost"],
    "research": ["research", "sources", "trends", "competitor"],
    "marketing": ["marketing", "seo", "campaign", "brand"],
    "sales": ["lead", "customer", "business", "sales", "outreach", "proposal"],
    "product": ["app", "website", "software", "product", "build"],
    "finance": ["finance", "revenue", "expense", "invoice", "cashflow", "profit", "budget"],
    "operations": ["operations", "workflow", "sop", "schedule", "vendor", "procurement"],
    "after-sales": ["after-sales", "support", "feedback", "renewal", "retention", "warranty"],
}

def route_command(command: str) -> list[dict[str, Any]]:
    text = command.lower()
    routes = []
    for agent, capabilities in AGENT_CAPABILITIES.items():
        matches = [word for word in capabilities if word in text]
        if matches:
            routes.append({"agent": agent, "matched": matches})
    return routes or [{"agent": "ceo", "matched": ["general"]}]

def create_workflow(command: str, priority: str = "normal") -> dict[str, Any]:
    routes = route_command(command)
    workflow = {
        "id": f"wf-{uuid4().hex[:10]}", "command": command, "priority": priority,
        "status": "queued", "routes": routes, "created_at": datetime.now(timezone.utc).isoformat(),
        "steps": [{"step":i,"name":name,"status":"queued"} for i,name in enumerate(["Understand","Delegate","Execute","Verify","Report"],1)],
    }
    memory.remember("workflow", f"{workflow['id']}: {command}", "DIMRI CEO")
    return workflow
