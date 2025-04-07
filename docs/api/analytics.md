# Analytics

## 1. Usage history

`GET /v1/analytics/usage?entity_id=user_123&start=2024-10-01&end=2024-10-31`

**Response (200 OK)**
```json
{
    "data": [
        {
        "timestamp": "2024-10-05T12:00:00Z",
        "limit_id": "def_abc123",
        "used": 50
        }
    ]
}
```

## 2. Exhaustion forecast

`GET /v1/analytics/forecast?limit_id=def_abc123&entity_id=user_123`

**Response (200 OK)**
```json
{
    "days_remaining": 7,
    "estimated_exhaustion_date": "2024-10-12"
}
```