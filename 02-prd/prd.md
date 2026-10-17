# Product Requirements Document (PRD): AI Draft-and-Review Assistant

| Document Version | 1.0 (MVP) |
| :--- | :--- |
| **Status** | Approved for Delivery (Sprint 1–3) |
| **Product Area** | Core Builder / AI Scaffolding |
| **Author** | Associate Product Manager (Portfolio Case Study) |
| **Classification** | Independent Design Artifact (Hypotheses & Model Assumptions Clearly Labeled) |

---

## 1. Executive Summary & Problem Context

Building internal tools currently requires manual, repetitive configuration: selecting and connecting data sources, writing SQL queries, laying out components (tables, forms, buttons), and wiring parameters together. 

Non-technical operations analysts lack the SQL proficiency to build independently, creating ticket backlog for internal engineering teams. Meanwhile, software engineers lose high-leverage hours on boilerplate scaffolding. Generative AI can draft internal applications in seconds; however, organizations and developers resist black-box AI features because they cannot inspect, verify, or govern what changes in the application.

The **AI Draft-and-Review Assistant** solves this through a core architectural philosophy: **AI proposes, humans dispose.** The assistant converts plain-language requirements into an interactive, modular draft (queries + components), presenting a side-by-side diff where the builder reviews, accepts, or rejects each component individually before any change is saved to draft.

---

## 2. Target Users & Jobs To Be Done (JTBD)

> *Note: Target personas and user needs are labeled as initial **hypotheses** pending discovery interviews.*

| Persona (Hypothesis) | Technical Profile | Core Job To Be Done (JTBD) | Primary Pain Point |
| :--- | :--- | :--- | :--- |
| **Operations Analyst** *(Primary)* | Non-technical or low-code; deep operational context on business data (orders, inventory, fulfillment). | *When I need a dashboard or operational queue for my team, I want to describe it in plain English and receive a working initial draft so that I can start from something real.* | Blocked waiting on engineering for basic queries and tables. |
| **Internal-Tools Developer** | Technical; writes SQL, JavaScript, APIs. | *When AI assists my tool building, I want to inspect the exact SQL queries and component bindings before applying them so that I remain in full technical control.* | Black-box AI that overwrites existing work or writes untrusted code. |
| **Workspace Administrator** | Security & engineering leadership; accountable for compliance and RBAC. | *When users in my workspace leverage AI, I want AI to enforce existing table and row permissions upstream so that no data leak or unauthorized query occurs.* | Fear that generative models will bypass permissions or leak sensitive customer data. |

---

## 3. Goals, Assumptions & Non-Goals

### Product Goals (All Targets Labeled as Assumptions)

| Metric | Target (Assumption) | Baseline / Rationale |
| :--- | :---: | :--- |
| **Time to First Working App** | Median $\le$ 30 minutes | Reduces manual scaffolding cycle from hours/days to under an hour. |
| **Draft-to-Publish Conversion** | $\ge$ 40% of generated drafts reach published state | Ensures drafts are practical and relevant rather than discarded toys. |
| **Part-Level Acceptance Rate** | $\ge$ 60% of proposed parts accepted | Key trust indicator: builders selectively adopt what is accurate. |
| **Security & Permission Violations** | Exactly 0 violations | Strict zero-tolerance gate; verified by server-side validation. |

### Non-Goals (Scope Boundaries for v1)

- **No Multi-Page Architecture Generation:** v1 focuses on single-page operational views (table + filter + detail modal). Complex workflows are deferred.
- **No Direct Production Commits:** The assistant can **never** commit directly to a published production environment. All changes commit to a versioned draft.
- **No Model Training on Customer Data:** User prompts, schema metadata, and query structures are never used to fine-tune external models.
- **No Destructive Write/Delete Operations:** v1 generates read queries (`SELECT`) only. Form write actions (`INSERT`/`UPDATE`/`DELETE`) require manual binding in MVP.

---

## 4. MVP Scope Matrix

| In Scope (v1 MVP) | Deferred to v1.1 | Out of Scope (Future) |
| :--- | :--- | :--- |
| Single-prompt to structured draft (queries + layout) | Refine-by-chat iterative diffs | Multi-agent autonomous workflows |
| Side-by-side Diff Preview with per-part Accept/Reject | Natural language write/update queries | Automated UI end-to-end testing generation |
| Server-side Schema & RBAC validation | Custom styling & theme generation | Voice prompt interface |
| Transparent exclusion notice for unauthorized tables | Multi-table relational joins wizard | Automatic database indexing suggestions |
| Starter prompts matched to connected data sources | Branching and merge resolution | |
| Workspace-level audit event logging | | |

---

## 5. Non-Functional Requirements (NFRs)

- **Latency (Target Assumption):** p95 draft generation response time $\le$ 20 seconds.
- **Security & Authorization:** Role-based access control (RBAC) enforced server-side. Schemas are pruned before sending to the model provider.
- **Resilience & Fallback:** If the LLM provider times out or errors, the builder degrades gracefully with an actionable error modal offering pre-built templates.
- **Rate Limiting:** Default quota of 20 drafts per user per hour to prevent runaway API spend and abuse.
- **Observability:** 100% of generation, review, apply, and publish events emit structured telemetry to the analytics event log.

---

## 6. Key Dependencies & Open Questions

### Technical Dependencies
1. **Model Provider API:** OpenAI / Anthropic / Gemini structured output API.
2. **Schema Metadata Catalog:** Internal service that introspects connected data sources and exposes schema metadata without row data.
3. **Workspace Permissions Service:** Centralized RBAC engine to authenticate role permissions.
4. **App Versioning Engine:** Storage layer managing draft vs. published app state.

### Open Questions & Future Decisions
1. *Data Privacy & Model Inputs:* Should column-level value previews (sample enum values like order status) be permitted if workspace admin explicitly opts in?
2. *Pricing Strategy:* Will AI drafts be included in existing platform seat pricing, or metered as AI credits?
3. *Model Selection:* Do enterprise customers require bringing their own API keys (BYOK) or selecting specific cloud hosting regions?
