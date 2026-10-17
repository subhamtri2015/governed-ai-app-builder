# User Acceptance Testing (UAT) Checklist

Before deploying `flag_ai_builder_assistant` to any customer workspace, all gating checklist items must be signed off by QA and the Product Lead.

---

## Pre-Release Launch Sign-Off Checklist

- [ ] **1. Golden Set Benchmark Threshold Met**
  - All 30 prompts in `03-ai-eval/golden_set.md` executed against active database.
  - Valid-draft rate is $\ge 90\%$ (Assumption target).
  - First-draft usefulness scores average $\ge 1.50 / 2.00$.
- [ ] **2. Zero Permission Leaks Verified (Launch Blocker)**
  - Prompts 21, 22, 23, 24 tested under restricted `ops_analyst` role.
  - Server-side validator (`prototype/validate_draft.py`) produces exactly 0 unauthorized table exposures.
- [ ] **3. Telemetry Ingestion Verified**
  - Executed draft workflows emit structured rows to `ai_draft_events`.
  - All 4 lifecycle stages (`draft_created`, `draft_reviewed`, `draft_applied`, `app_published`) recorded with accurate timestamps and latency metrics.
  - `05-analytics/metrics.sql` queries run without syntax errors.
- [ ] **4. Feature Flag Toggling Verified**
  - Enabling flag displays AI assistant panel; disabling flag hides UI immediately without page reload.
  - Applications created during enabled state remain 100% operational when flag is turned off.
- [ ] **5. Audit Log Completeness**
  - Every applied change reflects exact user ID, workspace ID, timestamp, and array of accepted vs. rejected part IDs.
- [ ] **6. Help Center & API Documentation Signed Off**
  - Public documentation published explaining data privacy guardrails (zero customer row transmission).
  - Postman collection verified against mock/staging server.
