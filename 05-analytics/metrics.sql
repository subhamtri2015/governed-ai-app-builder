-- ====================================================================
-- AI Draft-and-Review Assistant: Core Product Metrics
-- ====================================================================

-- 1. Weekly Acceptance Rate (Part-level Trust Metric)
-- Target hypothesis: >= 60% of proposed parts accepted by human builders.
SELECT 
    DATE_TRUNC('week', created_at) AS week,
    ROUND(SUM(parts_accepted)::FLOAT / NULLIF(SUM(parts_proposed), 0) * 100, 2) AS acceptance_rate_pct,
    SUM(parts_accepted) AS total_parts_accepted,
    SUM(parts_proposed) AS total_parts_proposed
FROM ai_draft_events
WHERE event_type = 'draft_reviewed'
GROUP BY 1
ORDER BY 1;

-- 2. Draft-to-Publish Funnel Conversion
-- Measures drop-off across the four lifecycle stages.
SELECT 
    COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_created') AS created,
    COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_reviewed') AS reviewed,
    COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_applied') AS applied,
    COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'app_published') AS published,
    ROUND(COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'app_published')::FLOAT / 
          NULLIF(COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_created'), 0) * 100, 2) AS end_to_end_conversion_pct
FROM ai_draft_events;

-- 3. Median Time (Minutes) from First Draft to Published App (Per Draft)
-- Demonstrates speed improvement over manual scaffolding (Target: <= 30-180 min vs days).
WITH c AS (
    SELECT draft_id, MIN(created_at) AS t 
    FROM ai_draft_events 
    WHERE event_type = 'draft_created' 
    GROUP BY draft_id
),
p AS (
    SELECT draft_id, MIN(created_at) AS t 
    FROM ai_draft_events 
    WHERE event_type = 'app_published' 
    GROUP BY draft_id
)
SELECT 
    COUNT(*) AS published_drafts,
    percentile_cont(0.5) WITHIN GROUP (ORDER BY date_diff('minute', c.t, p.t)) AS median_minutes
FROM c 
JOIN p USING (draft_id)
WHERE p.t >= c.t;
