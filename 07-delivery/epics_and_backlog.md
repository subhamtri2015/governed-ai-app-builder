# Delivery Epics & Engineering Backlog

## 1. Epic Breakdown

| Epic Key | Epic Name | Strategic Goal | Technical Scope |
| :--- | :--- | :--- | :--- |
| **E1** | **Draft Generation Engine** | Enable reliable plain-language translation into query/component ASTs. | Schema metadata pruning, prompt templating, LLM provider integration, event instrumentation. |
| **E2** | **Review & Apply Experience** | Provide builder transparency and granular control over changes. | Side-by-side diff UI, per-part accept/reject toggle, atomic canvas injection. |
| **E3** | **Governance & Safety** | Protect tenant data, enforce RBAC, and satisfy enterprise IT requirements. | Server-side validation pipeline (`validate_draft.py`), permission exclusion notices, audit event log. |
| **E4** | **Onboarding & Acceleration** | Eliminate blank-canvas friction for non-technical analysts. | Dynamic starter prompts matched to schema entities, template gallery fallback. |

---

## 2. Prioritized User Story Backlog

> **Assumption Notice:**  
> All story point estimates below represent **engineering estimation assumptions** based on standard Fibonacci sizing (where 1 point $\approx$ 0.5–1 day of engineering effort).

| Story Key | Story Title | Epic | Story Points (Assumption) | Priority | Dependencies |
| :--- | :--- | :---: | :---: | :---: | :--- |
| **ST-101** | Schema metadata service & prompt compiler | E1 | 5 | P0 | Database connection service |
| **ST-102** | Asynchronous draft generation endpoint (`POST /v1/ai/app-drafts`) | E1 | 8 | P0 | ST-101 |
| **ST-103** | Telemetry and event tracking pipeline | E1 | 3 | P1 | ST-102 |
| **ST-201** | Server-side draft validation engine | E3 | 5 | P0 | ST-102 |
| **ST-202** | Diff preview modal with per-part checkboxes | E2 | 8 | P0 | ST-201 |
| **ST-203** | Apply accepted parts to versioned draft canvas | E2 | 5 | P0 | ST-202 |
| **ST-301** | Permission-aware filtering with transparent exclusion reasons | E3 | 8 | P0 | ST-101, ST-201 |
| **ST-302** | Immutable audit log service & table schema | E3 | 3 | P1 | ST-103 |
| **ST-401** | Context-aware starter prompts on assistant launch | E4 | 3 | P2 | ST-101 |
| **ST-402** | Hardened error fallback modal with starter templates | E4 | 2 | P2 | ST-102 |
| **Total** | | | **50 Points** | | |
