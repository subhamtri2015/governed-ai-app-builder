# Draft-and-Review AI Builder: A Product Case Study

> **One-Line Summary:** An AI assistant that turns a plain-language request into a reviewable draft of an internal tool (queries, tables, forms) inside a low-code platform, where a human accepts or rejects each part before anything goes live.

---

## Portfolio & Disclaimer Notice

- **Nature of Project:** This is a **self-initiated, original portfolio case study** designed to demonstrate core Associate Product Manager (APM) competencies: writing functional specifications, prioritizing using data and frameworks, designing API contracts, defining metrics and event schemas, planning engineering delivery, and crafting go-to-market enablement.
- **Independence:** This project is not affiliated with, nor performed for, any commercial company or client.
- **Assumptions:** All targets, volumes, RICE scores, and story-point estimates represent **illustrative planning assumptions**, explicitly labeled as such. User research personas and needs represent initial **hypotheses** pending live interview execution.
- **Public Data Sources:** Utilizes public datasets ([Olist Brazilian E-Commerce](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)) and publicly cited competitor documentation. Raw CSV data files and local databases are untracked via `.gitignore`. See [`data-sources.md`](file:///Users/subham/Desktop/IA-GET/data-sources.md) for data dictionary and licensing notes.

---

## Repository Structure & Quick Links

```
ai-app-builder-assistant/
├── README.md                      # Executive Case Study Summary (This Document)
├── data-sources.md                # Public Dataset Info & Ingestion Guide
├── 01-research/                   # Discovery Script, Findings Template & Competitor Analysis
│   ├── interview_script.md
│   ├── findings_template.md
│   └── competitor_analysis.md
├── 02-prd/                        # PRD, User Stories, and Functional Specifications
│   ├── prd.md
│   ├── user_stories.md
│   └── functional_specs.md
├── 03-ai-eval/                    # 30-Prompt Golden Set, Rubric & Guardrails
│   ├── golden_set.md
│   ├── rubric.md
│   └── guardrails.md
├── 04-api/                        # OpenAPI 3.0 Spec & Postman Collection
│   ├── api_specification.md
│   ├── openapi.yaml
│   └── draft_assistant.postman_collection.json
├── 05-analytics/                  # Telemetry Schema, Metrics SQL & Synthetic Generator
│   ├── schema.sql
│   ├── metrics.sql
│   ├── generate_events.py
│   ├── load_olist.py
│   └── run_metrics.py
├── 06-prioritization/             # RICE Framework & Strategic Overrides
│   └── RICE.md
├── 07-delivery/                   # Epics, Backlog, Sprint Plan & Release Tiers
│   ├── epics_and_backlog.md
│   ├── sprint_plan.md
│   └── release_plan.md
├── 08-qa-launch/                  # QA Test Plan, UAT Checklist & GTM Strategy
│   ├── test_plan.md
│   ├── uat_checklist.md
│   └── gtm_plan.md
├── 09-design/                     # Screen Wireframes & UI Specifications
│   ├── README.md
│   ├── screen_1_prompt_starter.svg
│   ├── screen_2_diff_preview.svg
│   └── screen_3_publish_confirmation.svg
└── prototype/                     # Working Python Prototype & Test Suite
    ├── validate_draft.py
    └── test_validate_draft.py
```

---

## 01. Problem & User Research

### Problem Statement (Hypothesis)
Building internal tools requires repetitive manual work: connecting data sources, writing SQL queries, laying out components, and wiring bindings. Non-technical operations teams depend on developers for routine scaffolding, while engineers lose high-leverage hours on boilerplate. 

Generative AI can draft a working tool in seconds, but **teams resist AI-generated apps because they cannot see or govern what changes**. Without visibility into queries and granular control over UI changes, teams risk data exposure and broken production tools.

### Research Plan & Interview Discovery
- **Plan:** 5 to 8 short interviews (20 minutes) with operations analysts, low-code developers, and engineering managers.
- **Artifacts:**
  - Full 10-question interview script: [`01-research/interview_script.md`](file:///Users/subham/Desktop/IA-GET/01-research/interview_script.md)
  - Interview synthesis & hypothesis tracking template: [`01-research/findings_template.md`](file:///Users/subham/Desktop/IA-GET/01-research/findings_template.md)

### Competitor Analysis (Publicly Sourced Facts Only)

| Platform | AI Creation Workflow | Control & Permissions | Human Checkpoint | Sourced Public Reference |
| :--- | :--- | :--- | :--- | :--- |
| **Retool** | Generates full-stack apps from a prompt using live data, and can edit existing apps. Introduced Assist as public beta. | Respects SSO, role-based access control, and data-level permissions by default. | AI workflow orchestration includes human approval guardrails. | [Retool Assist Docs](https://docs.retool.com/changelog/assist) & [Retool Apps](https://retool.com/apps) |
| **Appsmith** | Assistant suggests widgets, writes JavaScript, and generates queries; operates in parts rather than full-app generation. | Can be self-hosted, keeping platform and AI within customer infrastructure. | Canvas-level review inside builder. | [Appsmith AI Overview](https://www.b12.io/ai-directory/appsmith-ai/) |
| **Bubble** | Generates an initial application plan that the user reviews before the app is constructed. | Standard application permissions; plan review occurs before build. | Plan-level review before full generation. | [Bubble AI Agent Manual](https://manual.bubble.io/help-guides/ai/bubble-ai-agent/generate-apps-with-ai) |

### Core Strategic Opportunities Identified
1. **Component-Level Accept/Reject with Visible Diff:** Rather than all-or-nothing generation or abstract plan review, provide a granular side-by-side diff where users accept Part A (query) and Part B (table) while rejecting Part C (unneeded widget).
2. **"Explain, Don't Fail" Permission Handling:** When a user lacks access to a table, prune it upstream and explicitly explain why in the preview (*"Excluded 1 table (customers): Insufficient permissions"*), turning a confusing error into transparent security.
3. **Public Quality & Safety Telemetry:** Publish telemetry on valid-draft rates and acceptance percentages to build trust with enterprise IT and security administrators.

---

## 02. Product Requirements Document (PRD)

- **Product:** AI Draft-and-Review Assistant for Internal Tools.
- **Target Personas (Hypotheses):**
  - *Ops Analyst (Primary):* Non-technical, knows operational data, wants working tools fast.
  - *Internal-Tools Developer:* Technical, seeks less boilerplate, requires granular query control.
  - *Workspace Admin:* Accountable for data compliance and role-based permissions.
- **Core Jobs To Be Done (JTBD):**
  - *When I need an operational tool, I want a working first draft quickly so I can start from something real.*
  - *When AI proposes changes, I want to inspect exactly what changed so I can trust it.*
  - *When I manage a workspace, I want AI to respect table permissions so I don't create security risks.*
- **Goals (Targets Labeled as Planning Assumptions):**
  - Median time to first working app $\le 30$ minutes.
  - $\ge 40\%$ of AI-assisted drafts reach published state.
  - $\ge 60\%$ of proposed parts accepted (trust metric).
- **Non-Goals (v1):** Multi-page app generation, unreviewed production commits, training models on customer data, write/delete queries.
- **Scope:** Prompt-to-draft, diff preview with selective accept/reject, permission-aware schema filtering, starter prompts, and audit logging. (*Refine-by-chat deferred to v1.1*).
- **Full Specifications:** Read [`02-prd/prd.md`](file:///Users/subham/Desktop/IA-GET/02-prd/prd.md), [`02-prd/user_stories.md`](file:///Users/subham/Desktop/IA-GET/02-prd/user_stories.md), and [`02-prd/functional_specs.md`](file:///Users/subham/Desktop/IA-GET/02-prd/functional_specs.md).

---

## 03. AI Considerations, Evaluation & Guardrails

- **Guiding Principle:** **AI proposes, humans dispose.** The assistant operates as an advisory scaffolding agent.
- **Golden Evaluation Set (30 Prompts):**
  - 10 Simple (single table, direct operational views)
  - 10 Moderate (joins, aggregations, multi-component layouts)
  - 10 Adversarial / Guardrail (restricted tables, injection attempts, ambiguous requests)
  - *All 30 prompts validated against real Olist tables with zero email references.* See [`03-ai-eval/golden_set.md`](file:///Users/subham/Desktop/IA-GET/03-ai-eval/golden_set.md).
- **Evaluation Rubric (0 to 2 per dimension):** Structural validity, schema fidelity, permission compliance, and first-draft usefulness. See [`03-ai-eval/rubric.md`](file:///Users/subham/Desktop/IA-GET/03-ai-eval/rubric.md).
- **Failure Modes & Mitigations:**

| Failure Mode | Impact | Engineering Mitigation | Metric / Gate |
| :--- | :--- | :--- | :--- |
| **Hallucinated Column / Table** | Broken app | Server-side validation against database catalog prior to diff preview. | $\ge 90\%$ Valid Draft Rate |
| **Over-Broad Query** | Data exposure | AST query parsing, row limits (`LIMIT 100`), read-only queries only. | 0 Write Statements Allowed |
| **User Over-Trust in AI** | Subtle bugs | Mandatory diff review; plain-language summaries for all queries. | Part-level Checkbox UI |
| **Prompt Injection** | Policy bypass | Server-side RBAC prunes restricted metadata *before* calling the model. | **0 Permission Violations** |
| **High Model Cost** | Unit margin erosion | Schema pruning, context caching, and 20 drafts/hour rate limiting. | Cost per draft $\le \$0.04$ |

---

## 04. API Specification & Postman Collection

The API handles asynchronous draft creation, diff preview retrieval, atomic apply, and telemetry tracking.

### Core Endpoints

1. **`POST /v1/ai/app-drafts`** — Initiate asynchronous draft generation
   - Request: `{"prompt": "Build an approvals dashboard from orders", "datasource_id": "ds_123"}`
   - Response (`202 Accepted`): `{"draft_id": "dr_456", "status": "pending"}`
2. **`GET /v1/ai/app-drafts/{draft_id}`** — Fetch proposed parts and exclusions
   - Response (`200 OK`): Returns proposed `parts` array (queries, widgets) and `excluded` array (tables pruned with reasons).
3. **`POST /v1/ai/app-drafts/{draft_id}/apply`** — Apply accepted parts to versioned canvas
   - Request: `{"accepted_part_ids": ["q1", "c1"]}`
   - Response (`200 OK`): `{"app_version_id": "av_789", "applied": 2, "rejected": 0}`
4. **`POST /v1/ai/app-drafts/{draft_id}/events`** — Ingest telemetry event
   - Request: `{"event_type": "draft_reviewed", "parts_proposed": 4, "parts_accepted": 3}`
   - Response (`204 No Content`)

- **OpenAPI 3.0 Specification:** [`04-api/openapi.yaml`](file:///Users/subham/Desktop/IA-GET/04-api/openapi.yaml)
- **Postman Collection with Automated Tests:** [`04-api/draft_assistant.postman_collection.json`](file:///Users/subham/Desktop/IA-GET/04-api/draft_assistant.postman_collection.json)

---

## 05. Product Analytics, Schema & Telemetry Results

- **North Star Metric:** Weekly AI-assisted applications reaching published state.
- **Input Metrics:** Part-level acceptance rate ($\ge 60\%$), draft-to-publish conversion ($\ge 40\%$), repeat draft rate.
- **Guardrail Metrics:** Server validation error rate ($< 5\%$), permission leaks (hard zero), support tickets per 100 drafts ($\le 2$).

### Database Schema (`05-analytics/schema.sql`)
```sql
CREATE TABLE ai_draft_events (
    event_id BIGINT PRIMARY KEY,
    workspace_id TEXT NOT NULL,
    user_id TEXT NOT NULL,
    draft_id TEXT NOT NULL,
    event_type TEXT NOT NULL, -- 'draft_created', 'draft_reviewed', 'draft_applied', 'app_published'
    parts_proposed INT,
    parts_accepted INT,
    latency_ms INT,
    created_at TIMESTAMP NOT NULL DEFAULT now()
);
```

### Verified Analytical Results on DuckDB (1,143 Synthetic Events across 400 Drafts)

*Executed via `python3 05-analytics/run_metrics.py` against `data/olist.duckdb`:*

1. **Weekly Part-Level Acceptance Rate:** Averaging **74% to 80%**, safely exceeding the $\ge 60\%$ trust hypothesis.
2. **Draft-to-Publish Funnel:**
   - Drafts Created: **400** (100.0%)
   - Drafts Reviewed: **341** (85.2%)
   - Drafts Applied: **259** (64.8% of created | 76.0% of reviewed)
   - Apps Published: **143** (35.8% end-to-end | 55.2% of applied)
3. **Median Cycle Time to Publish:** **146.0 minutes** (~2.4 hours) from draft creation to published app.

---

## 06. Prioritization: RICE Framework & Strategic Overrides

All reach, impact, confidence, and effort figures represent **illustrative assumptions for a 1-quarter delivery cycle**:

| Feature | Reach (Assumption) | Impact (Assumption) | Confidence (Assumption) | Effort (Assumption) | RICE Score | Raw Rank | MVP Decision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Diff preview, accept/reject** | 800 | 2 | 90% | 2.0 PM | **720** | 1 | **Included (MVP)** |
| **Prompt-to-draft** | 800 | 3 | 80% | 3.0 PM | **640** | 2 | **Included (MVP - Prerequisite)** |
| **Permission-aware generation** | 800 | 3 | 70% | 3.0 PM | **560** | 3 | **Included (MVP - Launch Gate)** |
| **Templates & starter prompts** | 600 | 1 | 90% | 1.0 PM | **540** | 4 | **Included (MVP)** |
| **Refine by chat** | 500 | 2 | 70% | 2.0 PM | **350** | 5 | **Deferred to v1.1** |
| **Audit log** | 150 | 2 | 90% | 1.0 PM | **270** | 6 | **Included (MVP - Enterprise Gate)** |

### Strategic PM Overrides
1. **Dependency Override:** Prompt-to-draft ships before diff preview because diff review cannot function without draft generation.
2. **Security Launch Gate:** Permission-aware generation is a mandatory release gate because trust failures carry catastrophic blast radius.
3. **Enterprise Rollout Gate:** The audit log scores lowest mathematically (270) but is promoted to MVP because enterprise IT security will block rollout without compliance logging.
4. **Scope Discipline:** Refine by chat is deferred to v1.1 to keep MVP delivery tight and measurable.

See [`06-prioritization/RICE.md`](file:///Users/subham/Desktop/IA-GET/06-prioritization/RICE.md) for detailed rationale.

---

## 07. Delivery Plan & Sprints

- **Epics:** E1 Draft Generation, E2 Review & Apply, E3 Governance & Safety, E4 Onboarding.
- **Sprint Cadence (2-Week Sprints):**
  - **Sprint 1 (16 pts):** Schema metadata service, draft generation endpoint, telemetry event tracking.
  - **Sprint 2 (18 pts):** Server-side validation pipeline, diff preview UI, selective apply to versioned draft.
  - **Sprint 3 (16 pts):** Permission pruning with exclusions, audit log, starter prompts, team bug bash.
- **Release Tiers:** Phase 0 Bug Bash $\rightarrow$ Phase 1 Internal Alpha $\rightarrow$ Phase 2 Opt-In Beta (10 Workspaces) $\rightarrow$ Phase 3 General Availability.
- **Instant Rollback:** Feature flag `flag_ai_builder_assistant` toggles AI drawer off per workspace in $<30$ seconds without disrupting manual canvas tools or existing apps.

See [`07-delivery/epics_and_backlog.md`](file:///Users/subham/Desktop/IA-GET/07-delivery/epics_and_backlog.md) and [`07-delivery/sprint_plan.md`](file:///Users/subham/Desktop/IA-GET/07-delivery/sprint_plan.md).

---

## 08. QA, UAT & Go-To-Market Strategy

- **Test Plan:** 9 structured test scenarios covering happy paths, empty schemas, RBAC pruning, injection attempts, model timeouts, and concurrent editing. See [`08-qa-launch/test_plan.md`](file:///Users/subham/Desktop/IA-GET/08-qa-launch/test_plan.md).
- **Pre-Release UAT Checklist:** 6 mandatory launch verification gates including 0 permission leaks and telemetry logging verification. See [`08-qa-launch/uat_checklist.md`](file:///Users/subham/Desktop/IA-GET/08-qa-launch/uat_checklist.md).
- **Cross-Functional GTM Enablement Plan:** Actionable enablement deliverables for Customer Success (triage runbook), Sales (demo script & security one-pager), Marketing (video & changelog), and Support (macros). See [`08-qa-launch/gtm_plan.md`](file:///Users/subham/Desktop/IA-GET/08-qa-launch/gtm_plan.md).

---

## 09. Risk Management Matrix

| Risk Identified | Severity | Product Mitigation | Monitoring Metric |
| :--- | :---: | :--- | :--- |
| **Hallucinated Schema Output** | High | Server-side validation against database catalog (`validate_draft.py`) before diff preview. | Valid-Draft Rate ($\ge 90\%$) |
| **Sensitive Data Exposure** | Critical | Upstream schema pruning; zero row values sent to model provider. | Permission Leaks ($= 0$) |
| **User Over-Trust in AI** | Medium | Plain-language SQL summaries; per-component checkboxes; safe draft canvas isolation. | Edit Rate & Acceptance Rate |
| **Model Inference Costs** | Medium | Schema caching, context window pruning, 20 drafts/hour user quota. | Cost per draft ($\le \$0.04$) |
| **Blank-Canvas User Churn** | Medium | Dynamic schema-matched starter prompt pills on launch. | First-day draft creation rate |

---

## 10. Design & Visual Specifications

Three core interface designs documented in [`09-design/README.md`](file:///Users/subham/Desktop/IA-GET/09-design/README.md):
1. **Prompt Screen with Starter Prompts:** [`screen_1_prompt_starter.svg`](file:///Users/subham/Desktop/IA-GET/09-design/screen_1_prompt_starter.svg)
2. **Diff Preview with Per-Part Checkboxes & Exclusions:** [`screen_2_diff_preview.svg`](file:///Users/subham/Desktop/IA-GET/09-design/screen_2_diff_preview.svg)
3. **Publish Confirmation & Audit Summary:** [`screen_3_publish_confirmation.svg`](file:///Users/subham/Desktop/IA-GET/09-design/screen_3_publish_confirmation.svg)

---

## 11. Working Server-Side Validation Prototype

Located at [`prototype/validate_draft.py`](file:///Users/subham/Desktop/IA-GET/prototype/validate_draft.py).  
Demonstrates why validation must occur **server-side** rather than relying on prompt instructions alone.

### Run Prototype Locally:
```bash
python3 prototype/validate_draft.py
```

### Prototype Output:
```text
Validation Output for ops_analyst:
  Valid: False
  Errors:
    - q2: no permission for table 'customers' (role: ops_analyst)
    - q3: unknown columns ['discount'] in table 'orders'
```

### Run Unit Test Suite:
```bash
python3 -m unittest prototype/test_validate_draft.py
```

---

## 12. CV Project Description (How to Present This Work)

**AI Draft-and-Review Assistant (Product Management Case Study)**
- Authored end-to-end PRD, functional specifications, and user stories with BDD acceptance criteria for an AI-assisted internal tool builder with human-in-the-loop diff preview.
- Architected REST API contracts (OpenAPI 3.0 & Postman collection) and telemetry tracking plan (`schema.sql`, `metrics.sql`) evaluated across 1,143 synthetic usage events in DuckDB.
- Formulated an AI evaluation framework featuring a 30-prompt golden set, quality rubric, and a working Python server-side validation prototype enforcing role-based access control.
- Designed quarterly delivery backlog prioritized via RICE framework with documented strategic overrides for enterprise governance and safety gates.

---

## 13. Product Interview Defense & Preparation

1. **"Where did your numbers come from?"**  
   *"They are explicitly labeled illustrative planning assumptions for this case study. I defined the formulas, rationale, and tracking queries so every metric can be measured in a live deployment."*
2. **"What did you learn from user research interviews?"**  
   *"I strictly report only what real users say. In this portfolio project, personas and pain points are treated as discovery hypotheses, supported by ready-to-execute interview scripts and findings templates."*
3. **"Why did you override the raw RICE scores?"**  
   *"Prompt-to-draft is a foundational prerequisite for diff preview. Permission-aware filtering is a non-negotiable trust launch gate, and the audit log is an enterprise procurement requirement despite touching fewer users."*
4. **"How would you know the feature is succeeding post-launch?"**  
   *"By tracking our North Star metric—weekly AI-assisted apps reaching published state—paired with the part-level acceptance rate ($\ge 60\%$) and zero permission violations."*
5. **"What would you cut if your engineering timeline was halved?"**  
   *"I would cut starter prompts and defer the audit log for non-enterprise tiers, but I would never compromise on server-side schema and permission validation."*
