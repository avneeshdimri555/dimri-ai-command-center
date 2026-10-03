# DIMRI AI — Autonomous Company OS

DIMRI AI is a founder-controlled AI company operating system prototype.

## Current foundation
- Command Center dashboard
- DIMRI CEO / orchestrator
- 8 department routing capabilities
- Persistent SQLite company memory
- Durable task queue with task states
- Audit log
- 50 product/service catalog
- Founder approvals and Ghost Mode truth gate

## Backend
From the repository root:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000
```

Key endpoints: `/api/health`, `/api/brain`, `/api/brain/route`, `/api/commands`, `/api/workflows`, `/api/tasks`, `/api/memory`, `/api/audit`.

## Architecture

Founder → Web / Mobile / Telegram → DIMRI CEO → Company Brain → Persistent Memory + Task Queue → Department Agents → Tools/APIs → QA/Verification → Result → Memory.

## Control model

Consequential actions such as contracts, production deployments, money movement, major ad spend, credential changes and irreversible deletion remain approval-gated. The current backend does not execute external actions yet.

## Ghost Mode

REAL INFO FIRST: Source → Evidence → Verification → Claim → Script → QA → Publish. Unsupported factual claims must not be invented; creative material must be labeled.

## Roadmap
1. Unified Web/App/Telegram gateway
2. Authentication and role permissions
3. Model gateway and real agent execution
4. Tool/connectors layer
5. Ghost Mode source/evidence store
6. Human approval engine
7. Observability and production deployment

## Business structure

**Aishani Enterprises** is the parent organization. **DIMRI AI Command Center** is the future group-level control plane.

The six product workspaces are:
1. DIMRI Model & Fan Studio
2. DIMRI Digital Products Studio
3. DIMRI Social Studio (YouTube, Instagram and Facebook)
4. DIMRI Education Studio
5. DIMRI Apps & SaaS Studio
6. DIMRI Digital Services Studio

**Aishani World** remains a distinct kids' entertainment IP/brand; its product scope is maintained separately from the realistic-human Model & Fan Studio.

Each product is to have its own focused requirements, codebase/workspace, data boundaries, CEO assistant, QA and release lifecycle. A Group CEO will consolidate verified product reports and founder approvals after the individual products are ready. This is a target architecture, not a claim that all six products or their CEOs are implemented.

Shared support functions include Research & Insights, Marketing & Growth, Finance, Operations & QA, IT & Security, Sales & Partnerships, Customer Support, Legal & Compliance, Content & Creative, and HR & Agent Management.

See:
- `docs/AISHANI_ENTERPRISES_STRUCTURE.md` — existing operating map
- `docs/PRODUCT_ISOLATION_AND_CEO_ARCHITECTURE.md` — approved product separation, per-product CEO, live voice requirements, and integration acceptance gates

## Current integration foundation

The backend exposes `/api/pillars`, `/api/apps`, `/api/integrations`, `/api/marketplaces` and digital-product factory endpoints. Real credentials are supplied through environment secrets; no production secrets are committed.
