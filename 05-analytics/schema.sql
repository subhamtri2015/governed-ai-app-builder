-- AI Draft-and-Review Assistant: Analytics Schema
-- Captures the complete draft lifecycle for product adoption, latency, trust, and funnel analysis.

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
