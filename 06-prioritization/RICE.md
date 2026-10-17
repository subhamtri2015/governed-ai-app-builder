# Product Prioritization: RICE Framework

The RICE scoring model ($\text{Score} = \frac{\text{Reach} \times \text{Impact} \times \text{Confidence}}{\text{Effort}}$) was utilized to evaluate candidate features for the quarterly planning cycle.

> **Assumption Notice:**  
> All reach volumes, impact weights, confidence ratings, and person-month effort figures represent **illustrative planning assumptions** for a 1-quarter delivery window.

---

## 1. RICE Scoring Matrix

| Feature | Reach (Assumption: Users / Qtr) | Impact (Assumption: 1–3 Scale) | Confidence (Assumption: % Rating) | Effort (Assumption: Person-Months) | RICE Score | Raw Rank | MVP Decision |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **Diff preview, accept/reject** | 800 | 2 (High) | 90% | 2.0 PM | **720** | 1 | **Included (MVP)** |
| **Prompt-to-draft** | 800 | 3 (Massive) | 80% | 3.0 PM | **640** | 2 | **Included (MVP - Prerequisite)** |
| **Permission-aware generation** | 800 | 3 (Massive) | 70% | 3.0 PM | **560** | 3 | **Included (MVP - Launch Gate)** |
| **Templates and starter prompts** | 600 | 1 (Low) | 90% | 1.0 PM | **540** | 4 | **Included (MVP)** |
| **Refine by chat** | 500 | 2 (High) | 70% | 2.0 PM | **350** | 5 | **Deferred to v1.1** |
| **Audit log** | 150 | 2 (High) | 90% | 1.0 PM | **270** | 6 | **Included (MVP - Enterprise Gate)** |

---

## 2. Strategic Overrides & PM Rationale

A critical responsibility of an Associate Product Manager is understanding when quantitative ranking must yield to **architectural dependencies, safety guardrails, and enterprise buyer requirements**. 

The raw mathematical ranking was overridden in four specific instances:

### 1. Sequence Override: Prompt-to-Draft Ships Before Diff Preview
- **Raw Score:** 640 (Rank 2) vs 720 (Rank 1).
- **PM Rationale:** You cannot review a diff until a draft has been generated. While diff preview delivers high product differentiation, prompt-to-draft is the **foundational dependency** upon which all review and apply mechanisms operate.

### 2. Safety Override: Permission-Aware Generation is a Non-Negotiable Launch Gate
- **Raw Score:** 560 (Rank 3).
- **PM Rationale:** Trust failures in internal tools carry catastrophic blast radius. If an AI assistant generates queries exposing restricted compensation, customer data, or internal credentials, customer trust is permanently damaged. Even with a lower confidence rating (70%) due to multi-tenant complexity, permission-aware schema filtering is a mandatory release gate.

### 3. Enterprise Buyer Override: Audit Log Promoted to MVP Despite Lowest Score
- **Raw Score:** 270 (Rank 6 - Lowest).
- **PM Rationale:** Although the audit log touches fewer end-users (estimated reach of 150 admins/security leads vs. 800 builders), enterprise procurement and IT security teams will **block platform-wide rollout** without immutable telemetry. Investing 1.0 person-month unlocks rollout to enterprise accounts.

### 4. Scope Discipline: Refine by Chat Deferred to v1.1
- **Raw Score:** 350 (Rank 5).
- **PM Rationale:** Iterative multi-turn chat introduces state-machine complexity, conversational memory overhead, and substantial surface area for regressions. Deferring it to v1.1 keeps the MVP release tight, testable, and measurable against the core North Star metric.
