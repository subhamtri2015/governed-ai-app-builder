# UI/UX Design System & Screen Specifications

This folder contains high-fidelity interface designs, interaction flows, and UI component specifications for the **AI Draft-and-Review Assistant**.

---

## 1. Design System & Interaction Principles

1. **AI Proposes, Humans Dispose:** AI generations never auto-commit to live production apps. Every generated entity is staged in an interactive diff preview where builders exercise component-level governance.
2. **Transparent Boundaries ("Explain, Don't Fail"):** When role-based access control (RBAC) restricts table access, the UI presents an explicit, high-contrast banner explaining which tables were excluded and why, rather than failing silently.
3. **No Blank-Canvas Paralysis:** First-time builders are greeted with 5 schema-matched starter prompt pills to accelerate discovery.

---

## 2. Core UI Screens & Visual Artifacts

### Screen 1: Prompt & Starter Prompts Interface
*Location: [`screen_1_prompt_starter.svg`](file:///Users/subham/Desktop/IA-GET/09-design/screen_1_prompt_starter.svg)*
- **Purpose:** Empty-state builder drawer with connected data source selector (`PostgreSQL: Olist DB`), prompt input textarea, and 5 dynamic starter pills matched to active schema entities.
- **Key Elements:**
  - Clear RBAC badge (`Role: ops_analyst`).
  - Starter prompt pills (`✦ Order Fulfillment Queue`, `✦ Delayed Delivery Alert View`, `✦ Payment Method Breakdown`).
  - Privacy disclosure: *"Zero customer row data sent to model. Governed by workspace RBAC."*

---

### Screen 2: Granular Diff Preview & Permission Exclusions
*Location: [`screen_2_diff_preview.svg`](file:///Users/subham/Desktop/IA-GET/09-design/screen_2_diff_preview.svg)*
- **Purpose:** Core human-in-the-loop review modal. Displays proposed SQL queries and UI components side-by-side with individual checkboxes.
- **Key Elements:**
  - **Exclusion Alert Banner:** Highlighting pruned tables (*"Excluded 1 table (customers): Requires workspace admin permission"*).
  - **Component Checkboxes:** Part `q1` (Query) and Part `c1` (Table) checked; Part `c2` (Metric Card) unchecked by builder.
  - Plain-language query summaries translating SQL logic for non-technical analysts.

---

### Screen 3: Safe Canvas Isolation & Publish Confirmation
*Location: [`screen_3_publish_confirmation.svg`](file:///Users/subham/Desktop/IA-GET/09-design/screen_3_publish_confirmation.svg)*
- **Purpose:** Post-apply draft state showing rendered components on an isolated draft canvas (`Draft v1.4`), followed by an explicit 2-step publish confirmation modal.
- **Key Elements:**
  - Rendered operational table bound to live data.
  - Publish modal showing an audit release summary (2 parts accepted, 1 rejected, audit trail ID `aud_89312`).
  - Clear separation between draft canvas and production release.

---

## 3. Figma Design Specifications

- **Artboard Resolution:** Desktop 1440 × 900 px (Base scale: 1200 × 800 px SVG).
- **Color Palette:**
  - Surface Background: Slate 900 (`#0F172A`)
  - Elevated Cards: Slate 800 (`#1E293B`)
  - Accent / Primary Action: Royal Blue (`#2563EB` → `#1D4ED8`)
  - Success / Accepted: Emerald 500 (`#22C55E`)
  - Warning / Exclusions: Amber 500 (`#D97706` / `#451A03`)
  - Discarded / Danger: Rose 500 (`#EF4444`)
- **Typography:** Inter / System UI (`-apple-system`, `BlinkMacSystemFont`, `Segoe UI`, `Roboto`).
- **Figma Prototype Link:** Available in private workspace design tokens repository; wireframe vector exports preserved above for public repository viewing.
