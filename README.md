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
