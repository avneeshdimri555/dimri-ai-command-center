# DIMRI AI God Board — Free-First MVP Architecture

## Product hierarchy
- Aishani Enterprises: parent company and portfolio overview.
- DIMRI Digital Studio: operating studio for content, apps, digital commerce, and services.
- DIMRI AI — God Board: founder-controlled operating console and AI coordination layer.
- Three primary workspaces: Persona & Model Studio; Creator & UGC Studio; Social & Channel Studio.
- Shared control areas: AI CEO, agents, tasks, approvals, calendar, analytics, revenue & finance, integrations, audit/activity, settings.

## MVP scope
1. Responsive dashboard and client-side navigation between detailed workspace screens.
2. Persona/model records: identity profile, visual DNA, voice DNA, status, tags, linked campaigns.
3. Creator pipeline: briefs, scripts, assets, platform-specific output variants, review state.
4. Social registry: YouTube channels, Instagram accounts, Facebook Pages; distinguish registered metadata from authenticated connections.
5. Founder approval gate for publishing, spend, credentials, contracts, production deploys, and irreversible actions.
6. Agent roster and task dispatch. Until a model/tool worker is connected, dispatched tasks must be labelled queued and not represented as executed.
7. Activity log and operational reports based only on available system data.

## Free-first technical direction
- Keep the existing GitHub repository as the source of truth.
- Keep the current static website for the public studio site and dashboard UI.
- Use the existing FastAPI backend for APIs; the currently listed Render services are static sites, so a backend web service must be deployed separately before API-backed features can work.
- Avoid Supabase for MVP. SQLite is acceptable for local development and a single-instance prototype, but do not rely on a container's ephemeral filesystem for durable production data. Before multi-user or production use, choose a persistent database (e.g. a verified free Postgres tier or a paid persistent disk) and set backups/migrations.
- Store credentials only in server-side environment variables or a secrets manager; never in browser code, Git, or chat.
- Keep AI model inference, image/video generation, storage, and social APIs as replaceable provider adapters. A free UI/hosting tier does not mean model/API usage is free.
- No paid domain, hosting upgrade, API spend, or account purchase without founder approval.

## Digital-product payments (deferred)
- Phase 1: no checkout; create product catalog records and exportable product details.
- Phase 2 for India-first sales: evaluate a hosted Razorpay Payment Link/Page for UPI/cards, with manual delivery initially. Confirm current merchant eligibility, KYC, fee schedule, GST, refund and settlement terms before activation.
- Alternative hosted storefront: evaluate Instamojo for simpler listing/delivery; verify the current digital-product fee (not only the physical-product headline rate) before choosing.
- International storefronts (e.g. Gumroad/Payhip) require checking Indian seller onboarding, supported payouts, buyer payment methods, currency conversion, platform fees and tax handling before launch.
- YouTube/Meta monetization is paid by those platforms to the eligible creator/business account; it is not a universal instant withdrawal API for this dashboard. Track payouts as reported/imported data first; integrate official analytics and finance records later.
- Payments are not required to start the MVP and Stripe remains deferred as requested.

## Release stages
- Stage A: navigation, responsive UI, workspace detail screens, founder identity asset placement, empty states.
- Stage B: connect UI to FastAPI endpoints; verify API service deployment, health checks, persistent storage and audit log.
- Stage C: agent/model provider execution, evidence-backed research, asset generation and cost controls.
- Stage D: OAuth and official platform permissions; content preview, approval, scheduling, publish and analytics.
- Stage E: digital-product checkout, delivery, refunds, tax/accounting and reconciliation.

## Truthful status labels
Use Draft, Queued, Running, Needs Approval, Published, Failed, and Connected/Not Connected only when supported by actual runtime data. Clearly label mock/demo data. Never claim autonomous execution, live analytics, or a platform connection until verified end-to-end.
