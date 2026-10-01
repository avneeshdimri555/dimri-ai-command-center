# DIMRI AI — Company OS Architecture

## Mission
DIMRI AI is being built as an AI-native operating system for a company, not only as a dashboard.

## Core engines
1. DIMRI CEO / Orchestrator — founder commands, delegation, workflow control and reporting.
2. Ghost Mode Media Engine — real-information research, evidence, human-feel content, QA, approved publishing and analytics.
3. AI Business Acquisition Engine — prospect research, personalized outreach, qualification, proposals and CRM.
4. AI Service Delivery Engine — intake, research, production, QA, client review, delivery and support.

## Company Brain workforce hierarchy

The AI CEO reports to the founder and coordinates executive heads, division leads and specialist agents. These are role definitions in the workforce registry, not proof that each role is a separately running autonomous model.

### Executive / shared team
- AI CEO — company strategy, delegation, approvals and reporting.
- Research & Intelligence Head; Trends & Platform Intelligence Head.
- Innovation & R&D Head — technology scouting, experiments and prototypes.
- Marketing Head; Sales & Business Development Head.
- Finance Head, supported by Accounting & Bookkeeping, Invoicing & Payment Tracking, Cashflow & Budget, and Finance Audit & Tax Support agents.
- Technology & IT Head, Automation & Integration Head, Backup & Recovery Agent.
- Creative & Production Head; Editing & Post-Production Head.
- Quality & Review Head; Content Safety & Integrity Head; Security & Compliance Head; Legal & Rights Head.
- Operations Head and Operations Support Agent.
- Team Integration Agent; Communications Head; People & Workforce Head; Customer Success & Support Head; Business Analytics Head.

### Division teams
- Persona Studio Lead: Model Research, Face & Body Styling, Identity & Consistency, Model Content, Model Licensing, Social Growth Strategy, Lifestyle Continuity, Community Insights, Disclosure & Rights.
- Channel Network Lead: Channel Research, Content Ideas, Script & Storyboard, Brand & Identity, Editing, Video Production, SEO, Communication, Quality & Safety, Regional Adaptation & Localization, Series & Story Continuity, Social Publishing, Channel Analytics.
- Apps Portfolio Lead: App Research, Product Management, UI/UX, Coding, Testing, App Support, Incident & Continuity, Workforce Performance Tracking.
- Digital AI Services Lead: Services Research, Services Sales, Services Delivery.
- Digital Products Lead: Product Research, Digital Product Creation, Product Design, Listing & Marketplace, Delivery & Customer Support.
- Education Lead: Education Research, Curriculum, Education Content, Education Quality, Education Support.

Every specialist has an explicit reports_to relationship to a lead or executive head. Channel-specific briefs and persona-specific autopilot settings remain scoped to their selected channel/persona.

### Workforce tracking
The workforce registry is available through /api/workforce and /api/agents. Agent dispatch is recorded as queued work; task status is exposed through /api/tasks; submitted execution summaries are stored as agent reports and listed through /api/workforce/reports; audit events record supported system actions. These records track only events the running backend actually receives. They do not imply independent agent heartbeats, automatic SLA detection, live productivity measurement or autonomous execution unless those services are implemented and verified.

## Departments
- Content & Media
- Marketing & Growth
- Sales & Business
- Product & Development
- Operations & Support
- Finance
- Operations
- After-Sales & Retention

## Ghost Mode truth contract
Ghost Mode must never present invented information as fact.

Factual pipeline:
Source -> Evidence -> Verification -> Claim -> Script -> QA -> Publish

Flag or reject:
- fabricated statistics
- invented news
- fake reviews
- fake customer results
- fabricated citations
- unsupported factual claims

Creative or fictional content must be clearly labeled.

## Autonomy boundaries
Consequential actions remain permissioned, including contracts, production deployments, money movement, major ad spend, credential changes, irreversible deletion and external commitments.

## Current build
- responsive Command Center frontend
- department and agent views
- Ghost Mode truth gate UI
- growth and sales pipeline UI
- client delivery UI
- 50-product catalog
- approvals and activity
- FastAPI backend foundation

## Next integration layers
1. Model gateway
2. PostgreSQL + vector memory
3. Durable workflow queue
4. Auth + role permissions
5. Tool/connectors layer
6. Source/evidence store
7. Agent execution runtime
8. Observability/audit logs
9. Real channel integrations
10. Production deployment


## Expanded business back office

### Finance
Finance is a full department, not one bot:
- Finance Head
- Accounting
- Bookkeeping
- Invoicing
- Payment Tracking
- Cashflow
- Profit & Loss
- Budget
- Financial Reporting
- Pricing
- Cost Optimization
- Tax Preparation Support
- Finance Audit

AI may analyze and prepare financial work, while money movement and other consequential financial actions require explicit authorization.

### Operations
Operations is the internal coordination layer:
- Operations Head
- Workflow Coordinator
- Project Operations
- Scheduling
- SOP Manager
- Knowledge Operations
- Automation Monitor
- Incident Response
- Vendor Operations
- Procurement

### After-Sales & Retention
After delivery, the company continues the customer lifecycle:
- After-Sales Service
- Customer Feedback
- Retention
- Renewal
- Warranty & Support

Lifecycle:
Lead -> Sale -> Onboarding -> Delivery -> After-Sales -> Renewal -> Expansion
