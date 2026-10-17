# Release & Rollout Strategy

## 1. Staged Release Tiers

```
[Phase 0: Team Bug Bash] ──> [Phase 1: Internal Alpha] ──> [Phase 2: Opt-In Beta] ──> [Phase 3: General Availability]
  (All 30 Golden Prompts)       (Internal Dogfooding)         (10 Target Workspaces)        (Platform-Wide Rollout)
```

| Phase | Target Audience | Duration | Gating Exit Criteria (All Labeled as Assumptions) |
| :--- | :--- | :--- | :--- |
| **Phase 0: Benchmark & Bug Bash** | Engineering + PM + QA | 2 Days | - 100% of 30 Golden Set prompts evaluated.<br>- Valid-draft rate $\ge 90\%$.<br>- Exactly 0 permission leaks. |
| **Phase 1: Internal Alpha** | Internal Solutions Architects & Ops | 2 Weeks | - p95 generation latency $\le 20$ seconds.<br>- Zero unhandled 500 errors across 100+ internal sessions. |
| **Phase 2: Opt-In Beta** | 10 Selected Customer Workspaces (Behind feature flag `flag_ai_builder_v1`) | 3 Weeks | - Part-level acceptance rate $\ge 50\%$.<br>- Draft-to-publish conversion $\ge 30\%$.<br>- Support tickets $\le 2$ per 100 generated drafts. |
| **Phase 3: General Availability (GA)** | All self-serve & enterprise workspaces | Ongoing | - Platform SLA $\ge 99.9\%$.<br>- AI generation cost per draft $\le \$0.04$. |

---

## 2. Feature Flag Architecture & Instant Rollback

- **Flag Identifier:** `flag_ai_builder_assistant`
- **Granularity:** Configurable per workspace and per role.
- **Rollback SLA:** Instantaneous (< 30 seconds) via dynamic configuration toggle without requiring application redeployment or database migrations.
- **Blast Radius Containment:** If the feature flag is disabled:
  1. The AI generation drawer disappears from the builder UI.
  2. The manual builder remains 100% functional.
  3. Existing drafts and published applications created with AI assistance continue functioning without disruption.
