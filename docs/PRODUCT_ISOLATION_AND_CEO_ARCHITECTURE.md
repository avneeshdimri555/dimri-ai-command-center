# Aishani Enterprises — Product Isolation & CEO Architecture

Status: planning baseline; this document does not claim the individual products or their CEOs are implemented.

## Goal

Build each business product independently with its own focused requirements, code, data boundaries, tests, and release lifecycle. Integrate only after each product meets its acceptance criteria. The existing DIMRI AI Command Center remains the future group-level control plane; it must not become a place where all product-specific implementation is mixed together.

## Product workspaces

1. **DIMRI Model & Fan Studio** — realistic AI human models, model identity/Visual DNA, model shoots, image and video creation, voice, Instagram creator workflows, fan memberships, paid content, subscriptions, analytics, and creator/fan engagement.
   - Visual requirement: photorealistic human models only. Use the user's Eromiify and FanPro Studio screen/video references as design/workflow references when available in the product workspace.
   - Model creation supports text-only, optional reference-image upload, and existing-model selection. A master reference is never mandatory.
   - Distinguish UI live preview from actual AI generation/editing. Never represent a placeholder, queued task, or static preview as a generated result.
2. **DIMRI Digital Products Studio** — research, creation, packaging, mockups, listings, pricing, marketplace workflows, sales and revenue analytics. Preserve the user's previously discussed 100 digital-product ideas and research as source material when available.
3. **DIMRI Social Studio** — YouTube, Instagram and Facebook channels/pages; content planning, scripts, image/video production, scheduling, publishing, channel analytics and approval workflows.
4. **DIMRI Education Studio** — learning products, courses, AI learning support, assessments, progress and education-service workflows.
5. **DIMRI Apps & SaaS Studio** — app portfolio and product lifecycle, including VANI, DermaVeda, YOU AI and future applications.
6. **DIMRI Digital Services Studio** — UGC, video editing/post-production, automation, AI spokesperson/dubbing, client projects, delivery and recurring service operations.

**Aishani World** remains a distinct kids' entertainment IP/brand with its own age-appropriate creative requirements. Its placement and implementation scope should be confirmed in its dedicated product brief rather than merged into the realistic-human Model & Fan Studio.

## CEO and team model

Each product workspace is intended to have a dedicated **Product CEO assistant** that can:
- report current status from persisted, verifiable project data;
- summarize completed, in-progress, blocked and next tasks;
- identify requirements, risks, bugs, costs, approvals and dependencies;
- route work to that product's specialist agents/teams;
- maintain product-specific context without leaking unrelated product data;
- support conversational text interaction and, when voice services are configured, live voice interaction.

A **Group CEO / DIMRI Company Brain** in the future Command Center provides consolidated reporting across products, shared operations, cross-product dependencies and founder approvals. It must link to source records and distinguish verified state from recommendations or estimates.

### Shared support functions

Research & Insights; Marketing & Growth; Finance; Operations & QA; IT & Security; Sales & Partnerships; Customer Support; Legal & Compliance; Content & Creative; HR & Agent Management.

Shared functions may provide common services, but product data, permissions, task queues, release configuration and product-specific memory remain separated by default.

## CEO report contract

Each product CEO should report:
- product and reporting timestamp;
- status: not started / planning / building / testing / blocked / live;
- verified shipped features and links/commit references;
- work in progress and next actions;
- blockers, risks and required founder decisions;
- current integrations and their actual connection/health state;
- usage, cost and revenue only when backed by connected records;
- confidence/source notes for any estimate or unverified claim.

No fabricated progress, metrics, API connectivity, generation, publishing, or revenue. External actions such as publishing, spending, credential changes, contracts and destructive operations remain approval-gated.

## Separation and integration rules

- Give each product its own repository or clearly isolated deployable codebase, database/schema, environment configuration, API keys/secrets, tests and release process.
- Do not copy production secrets between products. Use scoped credentials and least-privilege permissions.
- Do not import one product's implementation into another merely to share a UI. Shared capabilities should be versioned contracts/services.
- Keep an integration adapter for each product. The group dashboard consumes approved status/report APIs rather than reaching into product databases.
- Integrate only after product-level QA, security review, mobile/desktop checks, operational documentation and founder acceptance.
- Preserve the existing Command Center and Render services during the transition; audit before modifying or replacing anything.

## Live conversation

Text chat is the baseline. Live voice requires a configured speech-to-text / speech-generation or realtime voice provider, consent and privacy handling, authenticated sessions, server-side secret storage, usage controls, and a tested interruption/error path. A voice button or visual waveform alone is not a working voice integration.

## Acceptance gate for each product

1. Approved product brief and visual references.
2. Feature and data-boundary map.
3. Working implementation with real integrations clearly distinguished from demo states.
4. Automated/manual QA results and responsive checks.
5. Security, privacy, permissions and approval checks.
6. Deployable build with health/status reporting and rollback notes.
7. Founder review and explicit approval to integrate.

## Current repository boundary

The existing `dimri-ai-command-center` repository is treated as the **group-level control-plane foundation and audit source**, not as proof that all six product studios or their individual CEOs are complete. Product-specific implementations should be isolated in their own repositories/workspaces before the final integration phase.
