# Error handling

**Error codes:**
- `4xx`: Client errors (invalid request, access denied).
- `5xx`: Server errors.

**Response body:**
```json
{
    "error": "LimitExceeded",
    "message": "The limit has been reached",
    "details": { "remaining": 0 }
}
```