# Administration

## 1. Forced reset

`POST /v1/admin/limits/reset`

**Request:**
```json
{
    "entity_type": "user",
    "entity_id": "user_123",
    "limit_id": "def_abc123"
}
```

**Response (200 OK)**

## 2. Audit of changes

`GET /v1/admin/audit-logs?action=update`

**Response (200 OK):**
```json
[
    {
        "timestamp": "2024-10-05T12:00:00Z",
        "user": "admin_1",
        "action": "update",
        "target": "def_abc123"
    }
]
```