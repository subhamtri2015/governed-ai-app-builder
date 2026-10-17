# API Specification: AI Draft-and-Review Assistant

## 1. Overview & Architecture

The API manages the lifecycle of AI draft generation, preview inspection, selective acceptance, and event telemetry.  
Base URL: `https://api.internal-builder.io/v1`

---

## 2. Endpoints Summary

| Method | Path | Summary | Key Request Headers / Body | Success Response |
| :--- | :--- | :--- | :--- | :--- |
| `POST` | `/v1/ai/app-drafts` | Initiate draft creation | `{"prompt": "...", "datasource_id": "..."}` | `202 Accepted` (`draft_id`, `status: pending`) |
| `GET` | `/v1/ai/app-drafts/{draft_id}` | Fetch draft & diff preview | N/A | `200 OK` (`parts`, `excluded` tables) |
| `POST` | `/v1/ai/app-drafts/{draft_id}/apply` | Apply selected parts | `{"accepted_part_ids": ["q1", "c1"]}` | `200 OK` (`app_version_id`, `applied`, `rejected`) |
| `POST` | `/v1/ai/app-drafts/{draft_id}/events` | Ingest telemetry event | `{"event_type": "draft_reviewed", ...}` | `204 No Content` |

---

## 3. Postman Collection & Automated Tests

A ready-to-import Postman collection is located at [`04-api/draft_assistant.postman_collection.json`](file:///Users/subham/Desktop/IA-GET/04-api/draft_assistant.postman_collection.json).

### Postman Test Script (`POST /v1/ai/app-drafts`):
```javascript
pm.test("returns 202 and a draft id", function () {
    pm.response.to.have.status(202);
    pm.expect(pm.response.json()).to.have.property("draft_id");
});

var jsonData = pm.response.json();
if (jsonData.draft_id) {
    pm.collectionVariables.set("draftId", jsonData.draft_id);
}
```

### Usage with Postman Mock Servers:
1. Import `04-api/draft_assistant.postman_collection.json` into Postman.
2. Select **Create Mock Server** from the collection menu.
3. Configure `baseUrl` environment variable to point to the mock URL.
4. Execute collection runner to verify end-to-end request flows.
*(Note: Mock request allowances and team member seats vary by Postman plan tier; check your individual account details for current limits).*
