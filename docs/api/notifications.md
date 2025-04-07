# Notifications

## 1. Setting up Notifications

`POST /v1/notifications/settings`

**Request body:**
```json
{
    "limit_id": "def_abc123",
    "thresholds": [80, 90, 100],
    "channels": ["slack", "email"],
    "webhook_url": "https://example.com/alert" // optional
}
```

**Response (201 Created)**
