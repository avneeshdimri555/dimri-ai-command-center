"""DIMRI AI internal agent roster and safe dispatch helpers.

These are in-house role definitions, not autonomous model instances. Dispatch
creates a durable task for later execution; it does not call an LLM or publish
content.
"""
from __future__ import annotations

from typing import Any

AGENTS: list[dict[str, Any]] = [
    {"id": "ceo", "name": "AI CEO", "department": "Management", "purpose": "Break founder requests into clear work and route them.", "capabilities": ["planning", "delegation", "reporting"]},
    {"id": "research", "name": "Research Bot", "department": "Intelligence", "purpose": "Prepare research tasks, source lists, and evidence notes.", "capabilities": ["research", "sources", "trends", "competitors"]},
    {"id": "ghost", "name": "Ghost QA Bot", "department": "Media", "purpose": "Check factual claims for evidence completeness and risk flags.", "capabilities": ["claim review", "evidence checklist", "content QA"]},
    {"id": "scriptwriter", "name": "Scriptwriter Bot", "department": "Media", "purpose": "Prepare scripts, captions, storyboards, and creative briefs.", "capabilities": ["scripts", "captions", "storyboards"]},
    {"id": "youtube", "name": "YouTube Operations Bot", "department": "Media", "purpose": "Organize channel and content operations for review.", "capabilities": ["channel operations", "content queue", "metadata"]},
    {"id": "marketing", "name": "Marketing Bot", "department": "Growth", "purpose": "Prepare SEO, campaign, brand, and promotion tasks.", "capabilities": ["SEO", "campaigns", "brand"]},
    {"id": "sales", "name": "Sales Bot", "department": "Commerce", "purpose": "Prepare lead research, proposals, and customer follow-up tasks.", "capabilities": ["leads", "proposals", "customer follow-up"]},
    {"id": "product", "name": "Product Builder Bot", "department": "Technology", "purpose": "Break app, website, and software work into implementation tasks.", "capabilities": ["apps", "websites", "software"]},
    {"id": "finance", "name": "Finance Bot", "department": "Operations", "purpose": "Organize budget, expense, revenue, and reporting tasks.", "capabilities": ["budget", "expenses", "revenue reports"]},
    {"id": "operations", "name": "Operations Bot", "department": "Operations", "purpose": "Prepare SOPs, schedules, workflows, and vendor tasks.", "capabilities": ["SOPs", "workflows", "scheduling"]},
]

def list_agents() -> list[dict[str, Any]]:
    """Return role definitions with transparent execution status."""
    return [{**agent, "state": "configured", "execution": "task_queue_only"} for agent in AGENTS]

def get_agent(agent_id: str) -> dict[str, Any] | None:
    return next((agent for agent in AGENTS if agent["id"] == agent_id), None)
