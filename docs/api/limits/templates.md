# Managing Limit templates

## 1. Creating a limit template

`POST /v1/limits/template`

**Description:** Creating a new limit template (for example, "100 requests per day").

**Request body:**
```json
{
    "name": "api_daily_limit",
    "type": "count", // count, time, hybrid
    "max_value": 1000,
    "reset_type": "daily", // daily, monthly, never
    "conditions": "user.plan == 'premium'", // optional
    "metadata": { "description": "API limit for premium users" }
}
```

**Response (201 Created):**
```json
{
    "id": "def_abc123",
    "name": "api_daily_limit",
    "type": "count",
    "max_value": 1000,
    "reset_type": "daily",
    "conditions": "user.plan == 'premium'",
    "created_at": "2024-10-05T12:00:00Z"
}
```

**Errors:**
- `400 Bad Request`: Incorrect parameters.
- `409 Conflict`: A template with that name already exists.

## 2. Getting a list of templates

`GET /v1/limits/template?page=1&limit=10`

**Description:** Getting a list of paginated templates.

**Response (200 OK):**
```json
{
    "data": [
        {
        "id": "def_abc123",
        "name": "api_daily_limit",
        "type": "count",
        "max_value": 1000,
        "reset_type": "daily"
        }
    ],
    "total": 1,
    "page": 1
}
```

## 3. Getting template by id

`GET /v1/limits/template/{template_id}`

**Response (200 OK):**
```json
{
    "id": "def_abc123",
    "name": "api_daily_limit",
    "type": "count",
    "max_value": 1000,
    "reset_type": "daily"
}
```

**Errors:**
- `404 Not Found`: The template was not found.

## 4. Updating the template

`PUT /v1/limits/template/{template_id}`

**Request body:**
```json
{
    "max_value": 2000,
    "reset_type": "monthly"
}
```

**Response (200 OK):**
```json
{
    "id": "def_abc123",
    "name": "api_daily_limit",
    "type": "count",
    "max_value": 2000,
    "reset_type": "monthly"
}
```

**Errors:**
- `400 Bad Request`: Incorrect parameters.
- `404 Not Found`: The template was not found.

## 5. Deleting a template

`DELETE /v1/limits/template/{template_id}`

**Response (204 No Content)**

**Errors:**
- `400 Bad Request`: The template is used in bindings.
- `404 Not Found`: The template was not found.