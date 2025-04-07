# Binding limits to entities

## 1. Setting an entity limit

`POST /v1/limits/assignments`

**Description:** Linking a limit to a user, organization, etc.

**Request body:**
```json
{
    "entity_type": "user", // user, org, etc.
    "entity_id": "user_123",
    "definition_id": "def_abc123",
    "override_value": 500 // optional
}
```

**Response (201 Created):**
```json
{
    "id": "assign_xyz789",
    "entity_type": "user",
    "entity_id": "user_123",
    "definition_id": "def_abc123",
    "current_usage": 0,
    "override_value": 500
}
```

**Errors:**
- `400 Bad Request`: Incorrect parameters.

## 2. Getting linked limits

`GET /v1/limits/assignments?entity_type=user&entity_id=user_123`

**Response (200 OK):**
```json
[
    {
        "id": "assign_xyz789",
        "definition_id": "def_abc123",
        "current_usage": 100,
        "override_value": 500,
        "last_reset": "2024-10-05T00:00:00Z"
    }
]
```

## 3. Removing the binding

`DELETE /v1/limits/assignments/{assignment_id}`

**Response (200 No Content)**

**Errors:**
- `404 Not Found`: The assignment was not found.
