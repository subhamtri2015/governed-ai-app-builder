# User Research Plan & Interview Script

> **Portfolio Notice & Hypothesis Disclaimer:**  
> All personas, problem statements, and pain points documented in this portfolio case study are **hypotheses**. In a professional product management workflow, requirements and prioritization are validated through direct discovery. When presenting this project, note that discovery scripts and templates are prepared here to recruit real participants.

---

## 1. Research Objectives

1. Understand the current end-to-end workflow and cycle times required to take an internal tool from request to production.
2. Identify the single slowest or most frustrating step in the internal tool building process.
3. Unpack trust blockers and failure modes users experience when using generative AI features to build applications.
4. Determine what level of transparency, diff visualization, and granular control users require before applying AI-generated configurations to live or draft applications.
5. Identify governance and permission boundaries required by engineering managers and workspace admins.

---

## 2. Target Participant Profile & Recruiting Plan

- **Target Sample Size:** 5 to 8 participants.
- **Session Duration:** 20 to 25 minutes per session.
- **Target Roles:**
  - *Ops Analysts / Business Users:* People who frequently request or build simple tools (dashboards, approval queues, customer lookups).
  - *Internal-Tools Engineers / Low-Code Developers:* Engineers responsible for scaffolding, data source connections, and maintaining internal tools.
  - *Engineering Managers / Workspace Admins:* Accountable for data compliance, RBAC, and production stability.
- **Recruitment Channels:** Developer communities (Discord, Reddit r/webdev, low-code user forums), peer networks, and professional communities.

---

## 3. Interview Script (10 Questions)

| # | Question | PM Rationale / What We're Listening For |
| :--- | :--- | :--- |
| **Q1** | Tell me about the last internal tool you built or asked someone to build. | Baseline context: complexity, data sources involved, tech stack. |
| **Q2** | How long did it take from the initial request to having something usable in production? | Cycle time benchmarks to validate the "time to first working app" hypothesis. |
| **Q3** | Which step was the slowest, most repetitive, or most frustrating? | Identifying the bottleneck: SQL query authoring, UI layout, RBAC wiring, or testing. |
| **Q4** | Have you used any AI tool or feature (e.g., Copilot, ChatGPT, in-app assistants) to speed this up? What happened? | Current state AI adoption, perceived strengths, and prompt patterns. |
| **Q5** | What did you not trust about the AI output? | Core trust friction: hallucinated schema, incorrect joins, lack of explainability. |
| **Q6** | What would you need to see before applying an AI-made change to an application? | Validating requirement for granular component-level diffs vs. all-or-nothing apply. |
| **Q7** | Who has to approve changes to apps that read or write sensitive company data? | Governance workflow, review layers, role separation. |
| **Q8** | What went wrong the last time an internal app touched the wrong data or broke in production? | Worst-case failure modes and blast-radius considerations. |
| **Q9** | If AI could reliably do one part of this workflow for you, which part would deliver the most value? | Feature prioritization signal (SQL generation vs. UI binding vs. form scaffolding). |
| **Q10**| What would make you immediately stop using an AI app-building assistant? | Critical churn triggers (data exposure, broken production app, silent errors). |
