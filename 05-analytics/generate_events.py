"""
05-analytics/generate_events.py
Generates realistic synthetic usage event logs for the AI Draft-and-Review Assistant.
Output: 05-analytics/ai_draft_events.csv (~1,143 events across 400 unique drafts)
Funnel target: 400 created -> 341 reviewed -> 259 applied -> 143 published
Median creation-to-publish duration: 144 minutes
"""

import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

def generate_events(output_path="05-analytics/ai_draft_events.csv"):
    random.seed(42)
    start_date = datetime(2024, 1, 8, 9, 0, 0)
    
    drafts = [f"dr_{i:04d}" for i in range(1, 401)]
    
    # Deterministic funnel transitions matching test specifications:
    # 400 drafts -> 341 reviewed -> 259 applied -> 143 published
    shuffled = list(drafts)
    random.shuffle(shuffled)
    reviewed_set = set(shuffled[:341])
    
    shuffled_reviewed = list(shuffled[:341])
    random.shuffle(shuffled_reviewed)
    applied_set = set(shuffled_reviewed[:259])
    
    shuffled_applied = list(shuffled_reviewed[:259])
    random.shuffle(shuffled_applied)
    published_set = set(shuffled_applied[:143])
    
    # Calibrate 143 time differences so percentile_cont(0.5) is exactly 144.0 minutes
    diffs = [int(random.gauss(144, 35)) for _ in range(143)]
    diffs = [max(20, d) for d in diffs]
    diffs.sort()
    diffs[70] = 144
    diffs[71] = 144
    random.shuffle(diffs)
    
    users = [f"usr_{u:03d}" for u in range(1, 35)]
    workspaces = [f"ws_{w:02d}" for w in range(1, 8)]
    
    events = []
    event_id = 1
    pub_idx = 0
    
    for i, d_id in enumerate(drafts):
        u = random.choice(users)
        w = random.choice(workspaces)
        t_create = start_date + timedelta(days=i // 8, hours=(i % 8) * 1.5, minutes=random.randint(0, 45))
        parts_prop = random.randint(2, 6)
        lat = random.randint(3500, 19500)
        
        # 1. draft_created
        events.append({
            "event_id": event_id,
            "workspace_id": w,
            "user_id": u,
            "draft_id": d_id,
            "event_type": "draft_created",
            "parts_proposed": parts_prop,
            "parts_accepted": "",
            "latency_ms": lat,
            "created_at": t_create.strftime("%Y-%m-%d %H:%M:%S")
        })
        event_id += 1
        
        # 2. draft_reviewed
        if d_id in reviewed_set:
            t_review = t_create + timedelta(minutes=random.randint(2, 12))
            parts_acc = random.randint(max(1, parts_prop - 2), parts_prop)
            events.append({
                "event_id": event_id,
                "workspace_id": w,
                "user_id": u,
                "draft_id": d_id,
                "event_type": "draft_reviewed",
                "parts_proposed": parts_prop,
                "parts_accepted": parts_acc,
                "latency_ms": "",
                "created_at": t_review.strftime("%Y-%m-%d %H:%M:%S")
            })
            event_id += 1
            
            # 3. draft_applied
            if d_id in applied_set:
                t_apply = t_review + timedelta(minutes=random.randint(1, 6))
                events.append({
                    "event_id": event_id,
                    "workspace_id": w,
                    "user_id": u,
                    "draft_id": d_id,
                    "event_type": "draft_applied",
                    "parts_proposed": parts_prop,
                    "parts_accepted": parts_acc,
                    "latency_ms": "",
                    "created_at": t_apply.strftime("%Y-%m-%d %H:%M:%S")
                })
                event_id += 1
                
                # 4. app_published
                if d_id in published_set:
                    delay = diffs[pub_idx]
                    pub_idx += 1
                    t_pub = t_create + timedelta(minutes=delay)
                    events.append({
                        "event_id": event_id,
                        "workspace_id": w,
                        "user_id": u,
                        "draft_id": d_id,
                        "event_type": "app_published",
                        "parts_proposed": parts_prop,
                        "parts_accepted": parts_acc,
                        "latency_ms": "",
                        "created_at": t_pub.strftime("%Y-%m-%d %H:%M:%S")
                    })
                    event_id += 1
                    
    # Write to CSV
    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "event_id", "workspace_id", "user_id", "draft_id", "event_type",
            "parts_proposed", "parts_accepted", "latency_ms", "created_at"
        ])
        writer.writeheader()
        writer.writerows(events)
        
    print(f"Generated {len(events)} synthetic events across {len(drafts)} drafts -> {output_path}")

if __name__ == "__main__":
    generate_events()
