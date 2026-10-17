"""
05-analytics/run_metrics.py
Executes analytical SQL queries from metrics.sql against data/olist.duckdb
and prints high-contrast terminal tables suitable for review, reporting, and portfolio artifacts.
"""

import duckdb
from pathlib import Path

def run_analytics():
    db_file = Path("data/olist.duckdb")
    if not db_file.exists():
        print("Database data/olist.duckdb does not exist. Run load_olist.py first.")
        return
        
    con = duckdb.connect(db_file.as_posix())
    
    print("=" * 80)
    print(" AI DRAFT-AND-REVIEW ASSISTANT: TELEMETRY & PRODUCT ANALYTICS REPORT")
    print("=" * 80)
    
    # 1. Weekly Acceptance Rate
    print("\n[1] WEEKLY PART-LEVEL ACCEPTANCE RATE (Trust Metric Target: >= 60%)")
    print("-" * 80)
    print(f"{'Week Starting':<16} | {'Accepted Parts':<15} | {'Proposed Parts':<15} | {'Acceptance Rate':<15}")
    print("-" * 80)
    res1 = con.execute("""
        SELECT 
            STRFTIME(DATE_TRUNC('week', created_at), '%Y-%m-%d') AS week,
            SUM(parts_accepted) AS accepted,
            SUM(parts_proposed) AS proposed,
            ROUND(SUM(parts_accepted)::FLOAT / NULLIF(SUM(parts_proposed), 0) * 100, 2) AS rate
        FROM ai_draft_events
        WHERE event_type = 'draft_reviewed'
        GROUP BY 1
        ORDER BY 1;
    """).fetchall()
    
    for row in res1:
        print(f"{row[0]:<16} | {row[1]:<15} | {row[2]:<15} | {row[3]:>6.2f}%")
        
    # 2. Conversion Funnel
    print("\n[2] DRAFT-TO-PUBLISH CONVERSION FUNNEL (Volume: 400 Initial Drafts)")
    print("-" * 80)
    res2 = con.execute("""
        SELECT 
            COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_created') AS created,
            COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_reviewed') AS reviewed,
            COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'draft_applied') AS applied,
            COUNT(DISTINCT draft_id) FILTER (WHERE event_type = 'app_published') AS published
        FROM ai_draft_events;
    """).fetchone()
    
    c, r, a, p = res2
    print(f"  Stage 1: Drafts Created     : {c:4d} (100.0%)")
    print(f"  Stage 2: Drafts Reviewed    : {r:4d} ({r/c*100:5.1f}% of created)")
    print(f"  Stage 3: Drafts Applied     : {a:4d} ({a/r*100:5.1f}% of reviewed | {a/c*100:5.1f}% of created)")
    print(f"  Stage 4: Apps Published     : {p:4d} ({p/a*100:5.1f}% of applied  | {p/c*100:5.1f}% end-to-end)")
    
    # 3. Median Time to Publish
    print("\n[3] MEDIAN CYCLE TIME: DRAFT CREATION TO APP PUBLISH")
    print("-" * 80)
    res3 = con.execute("""
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
    """).fetchone()
    
    print(f"  Total Published Apps Sampled: {res3[0]}")
    print(f"  Median Turnaround Time      : {res3[1]:.1f} minutes (~{res3[1]/60:.2f} hours)")
    print("=" * 80)
    con.close()

if __name__ == "__main__":
    run_analytics()
