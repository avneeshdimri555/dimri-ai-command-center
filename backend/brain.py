from datetime import datetime, timezone
from uuid import uuid4
from typing import Any

class CompanyMemory:
    def __init__(self):
        self.company = {
            "name": "DIMRI AI",
            "principles": ["real_info_first", "founder_controlled", "permissioned_actions"],
        }
        self.projects: dict[str, dict[str, Any]] = {}
        self.decisions: list[dict[str, Any]] = []
        self.knowledge: list[dict[str, Any]] = []

    def remember(self, kind: str, content: str, source: str = "system"):
        item = {"id": str(uuid4()), "kind": kind, "content": content, "source": source,
                "created_at": datetime.now(timezone.utc).isoformat()}
        self.knowledge.append(item)
        return item

    def add_decision(self, decision: str, rationale: str = ""):
        item = {"id": str(uuid4()), "decision": decision, "rationale": rationale,
                "created_at": datetime.now(timezone.utc).isoformat()}
        self.decisions.append(item)
        return item

    def context(self) -> dict[str, Any]:
        return {"company": self.company, "decisions": self.decisions[-20:], "knowledge": self.knowledge[-50:]}

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
        "id": f"wf-{uuid4().hex[:10]}",
        "command": command,
        "priority": priority,
        "status": "planned",
        "routes": routes,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "steps": [
            {"step": 1, "name": "Understand", "status": "queued"},
            {"step": 2, "name": "Delegate", "status": "queued"},
            {"step": 3, "name": "Execute", "status": "queued"},
            {"step": 4, "name": "Verify", "status": "queued"},
            {"step": 5, "name": "Report", "status": "queued"},
        ],
    }
    memory.remember("workflow", f"{workflow['id']}: {command}", "DIMRI CEO")
    return workflow
