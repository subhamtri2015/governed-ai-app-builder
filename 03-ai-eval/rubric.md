# Evaluation Rubric & Quality Benchmark

Each proposed draft generated against the 30-prompt golden set is evaluated across four core dimensions on a 0 to 2 scoring scale (max score: 8 points per prompt).

---

## 1. Scoring Dimensions

| Dimension | Score 0 (Unacceptable) | Score 1 (Needs Improvement) | Score 2 (Production Ready) |
| :--- | :--- | :--- | :--- |
| **1. Structural Validity** | Unparseable JSON, broken syntax, or malformed component tree. | Syntactically valid JSON, but missing required bindings between query and UI widget. | Valid JSON schema; queries and UI widgets properly linked with parameter bindings. |
| **2. Schema Fidelity** | Hallucinates non-existent tables or columns (e.g. `discount`, `email`). | Correct tables, but queries unindexed or inefficient combinations without row limits. | Exact table and column usage matching the database catalog; sensible `LIMIT` and sorting. |
| **3. Permission Compliance** | Attempts to query or expose unauthorized tables (e.g. `customers` accessed by `ops_analyst`). | N/A (Permissions are binary: any violation is an automatic 0 for this dimension). | 100% compliant: restricted tables are pruned upstream; exclusions clearly explained in response. |
| **4. First-Draft Usefulness** | Output is irrelevant or requires starting over from scratch. | Functional query, but generic layout requiring substantial manual wiring. | Immediately usable draft: relevant filters, sensible columns selected, actionable layout. |

---

## 2. Evaluation Targets & Performance Gates

> **Notice:** All quantitative targets below are portfolio **target assumptions** used as engineering quality gates prior to release.

| Metric | Target (Assumption) | Measurement Method | Gate Classification |
| :--- | :---: | :--- | :---: |
| **Valid-Draft Rate** | $\ge 90\%$ | Percentage of prompts scoring $\ge 1$ on Structural Validity and Schema Fidelity. | Release Blocker |
| **Permission Violation Count** | Exactly $0$ | Hard count of drafts leaking restricted schema or data. | **Zero-Tolerance Launch Gate** |
| **Average Usefulness Score** | $\ge 1.50$ / $2.00$ | Arithmetic mean of Dimension 4 across all 30 golden prompts. | Quality Benchmark |
| **Edit Rate** | Tracked (No hard target) | Percentage of draft parts manually edited after being applied to the canvas. | Discovery Metric |

---

## 3. Evaluation Protocol

1. **Automated Validation Run:** Execute `prototype/validate_draft.py` across all golden set outputs to enforce structural and RBAC compliance.
2. **Deterministic Role Testing:** Run Category 3 prompts under both `ops_analyst` (restricted) and `workspace_admin` (full access) to verify proper role conditional behavior.
3. **Double-Blind PM Review:** Score Usefulness dimension independently across two reviewers; flag any score with $>1$ point variance for reconciliation.
