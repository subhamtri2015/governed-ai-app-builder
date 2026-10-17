"""
Unit tests for prototype/validate_draft.py
Verifies server-side schema and RBAC permission checks.
"""

import unittest
from prototype.validate_draft import validate_draft

class TestValidateDraft(unittest.TestCase):

    def test_valid_draft_allowed_role(self):
        draft = {
            "queries": [
                {"id": "q1", "table": "orders", "columns": ["order_id", "order_status", "order_purchase_timestamp"]},
                {"id": "q2", "table": "order_items", "columns": ["order_id", "price", "freight_value"]}
            ]
        }
        res = validate_draft(draft, "ops_analyst")
        self.assertTrue(res["valid"])
        self.assertEqual(len(res["errors"]), 0)

    def test_unauthorized_table_access(self):
        # Ops analyst attempting to query restricted customers or sellers tables
        draft = {
            "queries": [
                {"id": "q1", "table": "customers", "columns": ["customer_id", "customer_city"]}
            ]
        }
        res = validate_draft(draft, "ops_analyst")
        self.assertFalse(res["valid"])
        self.assertIn("no permission for table 'customers'", res["errors"][0])

    def test_unknown_table(self):
        draft = {
            "queries": [
                {"id": "q1", "table": "non_existent_table", "columns": ["id"]}
            ]
        }
        res = validate_draft(draft, "ops_analyst")
        self.assertFalse(res["valid"])
        self.assertIn("unknown table 'non_existent_table'", res["errors"][0])

    def test_unknown_columns(self):
        draft = {
            "queries": [
                {"id": "q1", "table": "orders", "columns": ["order_id", "discount_percentage", "coupon_code"]}
            ]
        }
        res = validate_draft(draft, "ops_analyst")
        self.assertFalse(res["valid"])
        self.assertIn("unknown columns", res["errors"][0])

    def test_admin_role_has_full_access(self):
        draft = {
            "queries": [
                {"id": "q1", "table": "customers", "columns": ["customer_id", "customer_unique_id"]},
                {"id": "q2", "table": "sellers", "columns": ["seller_id", "seller_city"]}
            ]
        }
        res = validate_draft(draft, "workspace_admin")
        self.assertTrue(res["valid"])
        self.assertEqual(len(res["errors"]), 0)

if __name__ == "__main__":
    unittest.main()
