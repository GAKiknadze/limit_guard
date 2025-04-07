# Checking and using limits

## 1. Check availability

`POST /v1/limits/check`

**Request body:**
```json
{
    "entity_type": "user",
    "entity_id": "user_123",
    "limit_id": "def_abc123",
    "context": { "exam_id": "math_2024" } // optional
}
```

**Response (200 OK):**
```json
{
    "allowed": true,
    "remaining": 400,
    "reset_time": "2024-10-06T00:00:00Z"
}
```

**Errors:**
- `403 Forbidden`: The limit has been reached.

## 2. Using the limit

`POST /v1/limits/consume`

**Request body:**
```json
{
    "entity_type": "user",
    "entity_id": "user_123",
    "limit_id": "def_abc123",
    "value": 1 // the amount to be debited
}
```

**Response (200 OK):**
```json
{
    "remaining": 399,
    "reset_time": "2024-10-06T00:00:00Z"
}
```

**Errors:**
- `400 Bad request`: Insufficient resource.

## 3. Reservation of the limit

`POST /v1/limits/reserve`

**Request body:**
```json
{
    "entity_type": "user",
    "entity_id": "user_123",
    "limit_id": "def_abc123",
    "value": 2,
    "ttl": 7200 // reserve lifetime in seconds
}
```

**Response (200 OK):**
```json
{
    "reservation_id": "res_456",
    "expires_at": "2024-10-05T14:00:00Z"
}
```

## 4. Reserve release

`POST /v1/limits/release`

**Request body:**
```json
{
    "reservation_id": "res_456",
    "value": 1 // optional (return of a part of the resource)
}
```
