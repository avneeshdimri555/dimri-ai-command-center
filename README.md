# DIMRI AI — Autonomous Company OS

DIMRI AI is a founder-controlled AI company operating system prototype.

## What is included

- Command Center dashboard
- DIMRI CEO / orchestrator concept
- 5 connected departments
- 58-agent workforce blueprint
- Ghost Mode with a real-information-first truth gate
- AI business acquisition workflow
- Client delivery workflow
- 50 product/service catalog
- Founder approvals and activity timeline
- Initial FastAPI backend foundation

## Frontend

The current frontend is intentionally lightweight and can run without external API credentials.

Run:

npm start

Open:

http://localhost:3000

## Backend foundation

From the repository root:

python3 -m venv .venv
source .venv/bin/activate
pip install -r backend/requirements.txt
uvicorn backend.main:app --reload --port 8000

Health endpoint:

http://localhost:8000/api/health

The backend currently exposes company, agent, command and workflow foundation endpoints. It does not yet execute real external actions.

## Ghost Mode rule

Ghost Mode uses a REAL INFO FIRST principle.

Factual content should follow:

Source -> Evidence -> Verification -> Claim -> Script -> QA -> Publish

The system should not invent statistics, news, reviews, customer results or citations. Creative/fictional material must be labeled clearly.

## Safety and control

Founder approval remains required for consequential actions such as contracts, production deployments, money movement, major ad spend, credential changes and irreversible deletion. Outreach should be personalized, permission-aware and compliant with applicable platform rules and anti-spam requirements.

## Architecture

See:

docs/DIMRI_AI_ARCHITECTURE.md

## Roadmap

1. Connect model gateway
2. Add persistent database and company memory
3. Add durable workflow orchestration
4. Add authentication and role permissions
5. Add tool/connectors layer
6. Build source/evidence store for Ghost Mode
7. Connect real agent execution
8. Add observability and audit logs
9. Add approved YouTube/Instagram/email/CRM integrations
10. Production deployment and controlled autonomy
