"""DIMRI AI workforce registry.

Role definitions are the organizational contract for the AI workforce. They are
not autonomous model instances by themselves: execution still requires a model,
tools, permissions, schedulers and a worker runtime.
"""
from __future__ import annotations
from typing import Any

CORE_TEAM: list[dict[str, Any]] = [
 {"id":"ceo","name":"AI CEO","department":"Core Leadership","level":"core","reports_to":"founder","purpose":"Company-wide planning, delegation, coordination and executive reporting.","capabilities":["strategy","planning","delegation","reporting","approvals"]},
 {"id":"research-head","name":"Research & Intelligence Head","department":"Core Intelligence","level":"core","reports_to":"ceo","purpose":"Coordinate company research and deliver sourced intelligence to every division.","capabilities":["research","sources","web discovery","competitive research","opportunity discovery"]},
 {"id":"trends-head","name":"Trends & Platform Intelligence Head","department":"Core Intelligence","level":"core","reports_to":"ceo","purpose":"Monitor connected platform data and permitted public signals for trends, audience behavior and content opportunities.","capabilities":["trend monitoring","platform analytics","audience signals","content opportunities"]},
 {"id":"marketing-head","name":"Marketing Head","department":"Core Growth","level":"core","reports_to":"ceo","purpose":"Coordinate organic growth, campaigns, positioning and approved advertising.","capabilities":["marketing","SEO","campaigns","brand","growth"]},
 {"id":"sales-head","name":"Sales & Business Development Head","department":"Core Growth","level":"core","reports_to":"ceo","purpose":"Coordinate lead discovery, qualification, proposals and authorized outreach.","capabilities":["lead research","qualification","proposals","CRM","outreach"]},
 {"id":"finance-head","name":"Finance Head","department":"Core Finance","level":"core","reports_to":"ceo","purpose":"Own company-wide revenue, expense, margin, budget and finance reporting.","capabilities":["revenue","expenses","budgets","margin","financial reporting"]},
 {"id":"technology-head","name":"Technology & IT Head","department":"Core Technology","level":"core","reports_to":"ceo","purpose":"Own platform architecture, infrastructure, integrations, deployments and technical health.","capabilities":["architecture","IT","integrations","deployment","monitoring"]},
 {"id":"creative-head","name":"Creative & Production Head","department":"Core Creative","level":"core","reports_to":"ceo","purpose":"Coordinate creative standards across image, video, audio, scripts and brand systems.","capabilities":["creative direction","production","visual standards","audio","scripts"]},
 {"id":"editing-head","name":"Editing & Post-Production Head","department":"Core Creative","level":"core","reports_to":"creative-head","purpose":"Coordinate editing, packaging, subtitles, thumbnails and final media preparation.","capabilities":["editing","post-production","subtitles","thumbnails","export"]},
 {"id":"quality-head","name":"Quality & Review Head","department":"Core Control","level":"core","reports_to":"ceo","purpose":"Independently review outputs against quality, evidence, identity, platform and workflow rules.","capabilities":["QA","review","evidence checks","identity consistency","release checks"]},
 {"id":"security-head","name":"Security & Compliance Head","department":"Core Control","level":"core","reports_to":"ceo","purpose":"Protect credentials, access, data, rights and high-risk actions.","capabilities":["access control","secrets","audit","privacy","rights checks"]},
 {"id":"operations-head","name":"Operations Head","department":"Core Operations","level":"core","reports_to":"ceo","purpose":"Coordinate SOPs, schedules, queues, incidents and cross-division execution.","capabilities":["operations","SOPs","scheduling","incident management","workflow"]},
 {"id":"automation-head","name":"Automation & Integration Head","department":"Core Technology","level":"core","reports_to":"technology-head","purpose":"Connect approved systems, schedulers, APIs and repeatable workflows.","capabilities":["automation","API workflows","schedulers","webhooks","connectors"]},
 {"id":"customer-head","name":"Customer Success & Support Head","department":"Core Growth","level":"core","reports_to":"ceo","purpose":"Coordinate customer onboarding, delivery communication, support and retention workflows.","capabilities":["onboarding","support","retention","feedback","service quality"]},
 {"id":"analytics-head","name":"Business Analytics Head","department":"Core Intelligence","level":"core","reports_to":"ceo","purpose":"Combine operational metrics into founder-ready dashboards and decision reports.","capabilities":["analytics","KPI reporting","dashboards","attribution","insights"]},
]

DIVISIONS: list[dict[str, Any]] = [
 {"id":"digital-ai-services","name":"Digital AI Services","lead":"services-lead","purpose":"External client services, UGC, AI content, automation and digital delivery."},
 {"id":"persona-studio","name":"DIMRI Persona Studio","lead":"persona-lead","purpose":"Adult AI persona and model creation, identity management, model content and commercial workflows."},
 {"id":"channel-network","name":"DIMRI Channel Network","lead":"channels-lead","purpose":"YouTube, Instagram and Facebook channel/account content operations, publishing and growth."},
 {"id":"apps","name":"DIMRI Apps","lead":"apps-lead","purpose":"AI app and SaaS product research, build, test, release and support."},
 {"id":"digital-products","name":"DIMRI Digital Products","lead":"commerce-lead","purpose":"E-books, stories, templates, forms, stickers, printables, prompt packs and other digital goods."},
 {"id":"education","name":"DIMRI Education","lead":"education-lead","purpose":"Courses, tutorials, learning products, workshops and education community."},
 {"id":"company-office","name":"Company Office & Shared Services","lead":"ceo","purpose":"Cross-company finance, resilience, workforce governance, legal, security, operations and coordination."},
]

DIVISION_AGENTS: list[dict[str, Any]] = [
 {"id":"services-lead","name":"Digital AI Services Lead","division":"digital-ai-services","role":"lead","purpose":"Own service pipeline, delivery and division reporting.","capabilities":["service catalog","client delivery","pricing"]},
 {"id":"services-research","name":"Services Research Agent","division":"digital-ai-services","role":"specialist","purpose":"Find relevant markets, prospects and service opportunities from permitted sources.","capabilities":["market research","prospect discovery","opportunity research"]},
 {"id":"services-sales","name":"Services Sales Agent","division":"digital-ai-services","role":"specialist","purpose":"Qualify prospects and prepare personalized, authorized outreach and proposals.","capabilities":["lead qualification","proposals","outreach"]},
 {"id":"services-delivery","name":"Services Delivery Agent","division":"digital-ai-services","role":"specialist","purpose":"Coordinate client deliverables, milestones and handoff.","capabilities":["project delivery","client briefs","handoff"]},
 {"id":"persona-lead","name":"Persona Studio Lead","division":"persona-studio","role":"lead","purpose":"Own model factory operations and persona reporting.","capabilities":["model operations","identity systems","campaign assignment"]},
 {"id":"persona-research","name":"Model Research Agent","division":"persona-studio","role":"specialist","purpose":"Research visual, fashion, creator and model-content trends using permitted sources.","capabilities":["model trends","style research","market research"]},
 {"id":"persona-creator","name":"Face & Body Styling Agent","division":"persona-studio","role":"specialist","purpose":"Configure adult fictional model appearance and approved visual identity parameters.","capabilities":["face","body styling","hair","fashion","appearance presets"]},
 {"id":"persona-identity","name":"Identity & Consistency Agent","division":"persona-studio","role":"specialist","purpose":"Maintain model identity records, reference sets, versioning and consistency checks.","capabilities":["identity lock","reference management","versioning","consistency"]},
 {"id":"persona-content","name":"Model Content Agent","division":"persona-studio","role":"specialist","purpose":"Prepare model images, videos, reels and UGC content plans.","capabilities":["image","video","UGC","content plans"]},
 {"id":"persona-licensing","name":"Model Licensing Agent","division":"persona-studio","role":"specialist","purpose":"Maintain commercial usage, licensing and collaboration records.","capabilities":["licensing","usage records","collaboration"]},
 {"id":"channels-lead","name":"Channel Network Lead","division":"channel-network","role":"lead","purpose":"Own multi-platform channel operations and reporting.","capabilities":["channel strategy","publishing","growth"]},
 {"id":"channel-research","name":"Channel Research Agent","division":"channel-network","role":"specialist","purpose":"Research channel topics, audience signals, competitors and content gaps.","capabilities":["topic research","competitors","content gaps"]},
 {"id":"channel-ideas","name":"Content Ideas Agent","division":"channel-network","role":"specialist","purpose":"Turn research and briefs into platform-specific content ideas.","capabilities":["ideas","hooks","formats","series"]},
 {"id":"channel-script","name":"Script & Storyboard Agent","division":"channel-network","role":"specialist","purpose":"Create scripts, storyboards and production briefs.","capabilities":["scripts","storyboards","captions"]},
 {"id":"channel-editor","name":"Channel Editing Agent","division":"channel-network","role":"specialist","purpose":"Coordinate editing, packaging, subtitles, thumbnails and final exports.","capabilities":["editing","thumbnails","subtitles","packaging"]},
 {"id":"channel-seo","name":"Channel SEO Agent","division":"channel-network","role":"specialist","purpose":"Prepare titles, descriptions, metadata and search-oriented packaging.","capabilities":["SEO","metadata","titles","descriptions"]},
 {"id":"channel-publisher","name":"Social Publishing Agent","division":"channel-network","role":"specialist","purpose":"Prepare scheduling and publishing actions for connected YouTube, Instagram and Facebook accounts.","capabilities":["scheduling","publishing","platform formatting"]},
 {"id":"channel-analytics","name":"Channel Analytics Agent","division":"channel-network","role":"specialist","purpose":"Analyze permitted platform analytics and report growth opportunities.","capabilities":["analytics","KPI analysis","growth recommendations"]},
 {"id":"apps-lead","name":"Apps Portfolio Lead","division":"apps","role":"lead","purpose":"Own app portfolio priorities, releases and reporting.","capabilities":["portfolio","roadmaps","release management"]},
 {"id":"apps-research","name":"App Research Agent","division":"apps","role":"specialist","purpose":"Discover market gaps, competitors, user needs and new product opportunities.","capabilities":["market research","competitors","opportunity discovery"]},
 {"id":"apps-product","name":"Product Manager Agent","division":"apps","role":"specialist","purpose":"Translate ideas into product requirements and acceptance criteria.","capabilities":["PRDs","requirements","roadmaps"]},
 {"id":"apps-ux","name":"UI/UX Agent","division":"apps","role":"specialist","purpose":"Define flows, interfaces and product experience.","capabilities":["UX","UI","prototypes"]},
 {"id":"apps-code","name":"Coding Agent","division":"apps","role":"specialist","purpose":"Implement software changes through approved development workflows.","capabilities":["coding","APIs","frontend","backend"]},
 {"id":"apps-test","name":"Testing Agent","division":"apps","role":"specialist","purpose":"Run tests, regression checks and release readiness reviews.","capabilities":["testing","QA","regression","release checks"]},
 {"id":"apps-support","name":"App Support Agent","division":"apps","role":"specialist","purpose":"Track bugs, support requests and product feedback.","capabilities":["support","bugs","feedback"]},
 {"id":"commerce-lead","name":"Digital Products Lead","division":"digital-products","role":"lead","purpose":"Own digital product catalog, production, listings and reporting.","capabilities":["catalog","product operations","sales"]},
 {"id":"commerce-research","name":"Product Research Agent","division":"digital-products","role":"specialist","purpose":"Research demand, niches, marketplaces and product opportunities.","capabilities":["market research","niche discovery","marketplaces"]},
 {"id":"commerce-creator","name":"Digital Product Creator Agent","division":"digital-products","role":"specialist","purpose":"Create e-books, stories, templates, forms, stickers, printables and prompt packs.","capabilities":["ebooks","templates","forms","stickers","printables","prompt packs"]},
 {"id":"commerce-design","name":"Product Design Agent","division":"digital-products","role":"specialist","purpose":"Create covers, layouts, graphics and product presentation assets.","capabilities":["design","layout","covers","graphics"]},
 {"id":"commerce-listing","name":"Listing & Marketplace Agent","division":"digital-products","role":"specialist","purpose":"Prepare product listings, metadata and marketplace publishing plans.","capabilities":["listings","SEO","marketplace operations"]},
 {"id":"commerce-delivery","name":"Delivery & Customer Agent","division":"digital-products","role":"specialist","purpose":"Coordinate digital delivery, customer support and order status.","capabilities":["delivery","orders","support"]},
 {"id":"education-lead","name":"Education Lead","division":"education","role":"lead","purpose":"Own education portfolio and learning product reporting.","capabilities":["curriculum","portfolio","learning products"]},
 {"id":"education-research","name":"Education Research Agent","division":"education","role":"specialist","purpose":"Research learning needs, topics, formats and competitor offerings.","capabilities":["learning research","topics","competitors"]},
 {"id":"education-curriculum","name":"Curriculum Agent","division":"education","role":"specialist","purpose":"Design courses, modules, lessons and learning paths.","capabilities":["curriculum","lessons","learning paths"]},
 {"id":"education-content","name":"Education Content Agent","division":"education","role":"specialist","purpose":"Produce scripts, worksheets, examples and supporting materials.","capabilities":["course content","worksheets","examples"]},
 {"id":"education-qa","name":"Education Quality Agent","division":"education","role":"specialist","purpose":"Review learning content for structure, clarity and completeness.","capabilities":["QA","review","learning quality"]},
 {"id":"education-support","name":"Education Support Agent","division":"education","role":"specialist","purpose":"Coordinate learner support, FAQs and feedback loops.","capabilities":["support","FAQs","feedback"]},
]


# Expanded executive functions requested for the Company Brain.
EXPANDED_CORE: list[dict[str, Any]] = [
 {"id":"innovation-head","name":"Innovation & R&D Head","department":"Core Innovation","level":"core","reports_to":"ceo","purpose":"Research new business models, emerging technologies, experiments and product opportunities; maintain an evidence-backed R&D pipeline.","capabilities":["innovation","R&D","experiments","technology scouting","prototypes"]},
 {"id":"operations-support","name":"Operations Support Agent","department":"Core Operations","level":"core","reports_to":"operations-head","purpose":"Handle day-to-day operational requests, SOP execution support, queue triage and cross-team follow-through.","capabilities":["operations support","SOPs","triage","follow-through"]},
 {"id":"backup-recovery","name":"Backup & Recovery Agent","department":"Core Resilience","level":"core","reports_to":"technology-head","purpose":"Track backup policies, recovery readiness, restore-test evidence and continuity incidents.","capabilities":["backup","recovery","restore testing","continuity"]},
 {"id":"content-safety-head","name":"Content Safety & Integrity Head","department":"Core Control","level":"core","reports_to":"quality-head","purpose":"Review content for age suitability, platform rules, privacy, disclosure, harmful claims and brand-specific safety boundaries.","capabilities":["content safety","policy review","privacy","disclosure","risk flags"]},
 {"id":"team-integration","name":"Team Integration Agent","department":"Core Coordination","level":"core","reports_to":"ceo","purpose":"Coordinate structured handoffs, dependencies, shared context and conflict resolution across agent teams.","capabilities":["team integration","handoffs","dependencies","coordination"]},
 {"id":"legal-rights-head","name":"Legal & Rights Head","department":"Core Governance","level":"core","reports_to":"ceo","purpose":"Flag legal, licensing, copyright, consent, contract and jurisdiction-specific issues for qualified human review.","capabilities":["legal issue spotting","copyright","licensing","contracts","rights"]},
 {"id":"people-workforce-head","name":"People & Workforce Head","department":"Core People","level":"core","reports_to":"ceo","purpose":"Maintain agent role definitions, workload allocation, onboarding instructions and workforce performance records.","capabilities":["workforce planning","role registry","capacity","onboarding","performance records"]},
 {"id":"communications-head","name":"Communications Head","department":"Core Communications","level":"core","reports_to":"ceo","purpose":"Coordinate internal agent communications and prepare approved external customer and partner communications.","capabilities":["communications","handoffs","customer messaging","partner updates"]},
]
EXPANDED_SPECIALISTS: list[dict[str, Any]] = [
 {"id":"finance-accounting","name":"Accounting & Bookkeeping Agent","division":"company-office","role":"specialist","purpose":"Organize transaction records, reconcile supplied financial data and prepare accounting summaries.","capabilities":["accounting","bookkeeping","reconciliation"],"reports_to":"finance-head"},
 {"id":"finance-invoice","name":"Invoicing & Payment Tracking Agent","division":"company-office","role":"specialist","purpose":"Prepare invoices and track payment status from connected, authorized records.","capabilities":["invoices","payment tracking","receivables"],"reports_to":"finance-head"},
 {"id":"finance-budget","name":"Cashflow & Budget Analyst","division":"company-office","role":"specialist","purpose":"Prepare cashflow forecasts, budgets, margin and expense analysis for review.","capabilities":["cashflow","budget","margin","forecasting"],"reports_to":"finance-head"},
 {"id":"finance-audit","name":"Finance Audit & Tax Support Agent","division":"company-office","role":"specialist","purpose":"Organize audit evidence and tax-preparation inputs for qualified review.","capabilities":["audit support","tax preparation support","controls"],"reports_to":"finance-head"},
 {"id":"innovation-scout","name":"Emerging Technology Scout","division":"apps","role":"specialist","purpose":"Track emerging technologies and assess evidence-backed fit for studio projects.","capabilities":["technology scouting","R&D","feasibility"],"reports_to":"innovation-head"},
 {"id":"innovation-experiments","name":"Innovation Experiments Agent","division":"apps","role":"specialist","purpose":"Design low-risk prototypes, experiments, success criteria and learning reports.","capabilities":["experiments","prototypes","validation"],"reports_to":"innovation-head"},
 {"id":"channel-brand","name":"Channel Brand & Identity Agent","division":"channel-network","role":"specialist","purpose":"Maintain each channel's brand guide, character bible, tone, visual continuity and audience promise.","capabilities":["brand","character bible","identity","continuity"],"reports_to":"channels-lead"},
 {"id":"channel-communication","name":"Channel Communication Agent","division":"channel-network","role":"specialist","purpose":"Prepare community posts, comment-response drafts and channel communication plans for approved use.","capabilities":["community","communications","response drafts"],"reports_to":"channels-lead"},
 {"id":"channel-quality","name":"Channel Quality & Safety Agent","division":"channel-network","role":"specialist","purpose":"Review scripts and assets for factual accuracy, child/family suitability where relevant, rights and platform policy.","capabilities":["quality","content safety","fact checks","policy"],"reports_to":"channels-lead"},
 {"id":"channel-video-production","name":"Video Production Agent","division":"channel-network","role":"specialist","purpose":"Convert approved scripts into shot lists, generation prompts, voiceover plans and production packages.","capabilities":["video production","shot lists","voiceover","production briefs"],"reports_to":"channels-lead"},
 {"id":"channel-regional","name":"Regional Adaptation & Localization Agent","division":"channel-network","role":"specialist","purpose":"Adapt approved content to selected languages and regional contexts without changing verified facts or character identity.","capabilities":["regional adaptation","localization","language QA"],"reports_to":"channels-lead"},
 {"id":"channel-story","name":"Series & Story Continuity Agent","division":"channel-network","role":"specialist","purpose":"Track recurring characters, episode canon, story arcs and non-repetition across channel series.","capabilities":["story continuity","series bible","episode tracking"],"reports_to":"channels-lead"},
 {"id":"persona-growth","name":"Persona Social Growth Strategist","division":"persona-studio","role":"specialist","purpose":"Research platform trends and plan organic, authentic audience development for each virtual persona.","capabilities":["social strategy","audience research","organic growth"],"reports_to":"persona-lead"},
 {"id":"persona-lifestyle","name":"Persona Lifestyle Continuity Agent","division":"persona-studio","role":"specialist","purpose":"Maintain a coherent fictional lifestyle calendar and ensure generated scenes do not misrepresent fictional events as real experiences.","capabilities":["lifestyle calendar","continuity","authenticity review"],"reports_to":"persona-lead"},
 {"id":"persona-community","name":"Persona Community Insights Agent","division":"persona-studio","role":"specialist","purpose":"Analyze permitted engagement signals and prepare genuine community interaction recommendations.","capabilities":["community insights","engagement analysis","response drafts"],"reports_to":"persona-lead"},
 {"id":"persona-safety","name":"Persona Disclosure & Rights Agent","division":"persona-studio","role":"specialist","purpose":"Check AI disclosure, consent, likeness permissions, usage rights and platform-specific publishing requirements.","capabilities":["AI disclosure","consent","likeness rights","policy review"],"reports_to":"persona-lead"},
 {"id":"resilience-incident","name":"Incident & Continuity Agent","division":"company-office","role":"specialist","purpose":"Maintain incident playbooks, outage notes, recovery actions and post-incident learning.","capabilities":["incident response","continuity","recovery"],"reports_to":"backup-recovery"},
 {"id":"workforce-tracking","name":"Workforce Performance Tracker","division":"company-office","role":"specialist","purpose":"Summarize assigned tasks, handoffs, reports, overdue work and agent-level delivery metrics from recorded system data.","capabilities":["task tracking","workload","SLA reporting","handoffs"],"reports_to":"people-workforce-head"},
]
CORE_TEAM.extend(EXPANDED_CORE)
DIVISION_AGENTS.extend(EXPANDED_SPECIALISTS)
# Explicit reporting lines for existing division specialists and leads.
for _agent in DIVISION_AGENTS:
 if "reports_to" not in _agent:
  _division = _agent.get("division")
  _lead = next((d["lead"] for d in DIVISIONS if d["id"] == _division), "ceo")
  _agent["reports_to"] = _lead

AGENTS = CORE_TEAM + DIVISION_AGENTS

def list_agents() -> list[dict[str, Any]]:
    return [{**a, "state":"configured", "execution":"task_queue_only"} for a in AGENTS]

def get_agent(agent_id: str) -> dict[str, Any] | None:
    return next((a for a in AGENTS if a["id"] == agent_id), None)

def workforce_summary() -> dict[str, Any]:
    return {
        "founder":"Avneesh Dimri",
        "parent_company":"Aishani Enterprises",
        "central_command":"AI CEO — God Board",
        "core_team":len(CORE_TEAM),
        "divisions":len(DIVISIONS),
        "division_leads":sum(1 for a in DIVISION_AGENTS if a["role"]=="lead"),
        "specialists":sum(1 for a in DIVISION_AGENTS if a["role"]=="specialist"),
        "total_configured_roles":len(AGENTS),
        "execution_mode":"task_queue_only",
    }
