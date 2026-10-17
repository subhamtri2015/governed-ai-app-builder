"""
prototype/validate_draft.py
Server-side validation prototype for the AI Draft-and-Review Assistant.

Enforces:
1. Strict schema compliance (verifies tables and columns against database catalog).
2. Role-based access control (RBAC) preventing unauthorized table access.
3. Clean error payloads informing builder preview diffs and admin guardrails.
"""

# Real schema catalog derived from the verified Olist database
SCHEMA = {
    "orders": [
        "order_id", "customer_id", "order_status", "order_purchase_timestamp",
        "order_approved_at", "order_delivered_carrier_date",
        "order_delivered_customer_date", "order_estimated_delivery_date"
    ],
    "order_items": [
        "order_id", "order_item_id", "product_id", "seller_id",
        "shipping_limit_date", "price", "freight_value"
    ],
    "order_payments": [
        "order_id", "payment_sequential", "payment_type",
        "payment_installments", "payment_value"
    ],
    "products": [
        "product_id", "product_category_name", "product_name_lenght",
        "product_description_lenght", "product_photos_qty", "product_weight_g",
        "product_length_cm", "product_height_cm", "product_width_cm"
    ],
    "customers": [
        "customer_id", "customer_unique_id", "customer_zip_code_prefix",
        "customer_city", "customer_state"
    ],
    "sellers": [
        "seller_id", "seller_zip_code_prefix", "seller_city", "seller_state"
    ],
    "order_reviews": [
        "review_id", "order_id", "review_score", "review_comment_title",
        "review_comment_message", "review_creation_date", "review_answer_timestamp"
    ]
}

# Role-based permissions matrix
ALLOWED = {
    "ops_analyst": ["orders", "order_items", "order_payments", "products"],
    "internal_dev": ["orders", "order_items", "order_payments", "products", "customers", "sellers", "order_reviews"],
    "workspace_admin": list(SCHEMA.keys())
}

def validate_draft(draft: dict, role: str) -> dict:
    """
    Validates an AI-proposed draft against the schema catalog and user role permissions.
    """
    errors = []
    allowed = set(ALLOWED.get(role, []))
    
    for q in draft.get("queries", []):
        table = q.get("table")
        qid = q.get("id", "unknown")
        
        # 1. Unknown table check
        if table not in SCHEMA:
            errors.append(f"{qid}: unknown table '{table}'")
            continue
            
        # 2. Permission check
        if table not in allowed:
            errors.append(f"{qid}: no permission for table '{table}' (role: {role})")
            continue
            
        # 3. Unknown column check
        bad_cols = [c for c in q.get("columns", []) if c not in SCHEMA[table]]
        if bad_cols:
            errors.append(f"{qid}: unknown columns {bad_cols} in table '{table}'")
            
    return {
        "valid": len(errors) == 0,
        "errors": errors
    }

if __name__ == "__main__":
    # Test draft containing:
    # - q1: valid query on allowed 'orders' table
    # - q2: unauthorized query on 'customers' table (restricted for ops_analyst)
    # - q3: hallucinated column 'discount' on 'orders' table
    sample_draft = {
        "queries": [
            {"id": "q1", "table": "orders", "columns": ["order_id", "order_status"]},
            {"id": "q2", "table": "customers", "columns": ["customer_id", "customer_city"]},
            {"id": "q3", "table": "orders", "columns": ["discount"]}
        ]
    }
    
    result = validate_draft(sample_draft, "ops_analyst")
    print("Validation Output for ops_analyst:")
    print(f"  Valid: {result['valid']}")
    print("  Errors:")
    for err in result["errors"]:
        print(f"    - {err}")
