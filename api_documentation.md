# Subscription Service & User Management API Documentation

Base URL: `/api/`

Authentication: **JWT Bearer Token**  
Header:  `Authorization: Bearer <access_token>`

---

## 1. User Management

### 1.1 Register a New User
- **Path:** `POST /api/accounts/`
- **Auth:** Public
- **Payload:**
```json
{
  "username": "johndoe",
  "email": "johndoe@example.com",
  "password": "StrongPassword123!",
  "first_name": "John",
  "last_name": "Doe"
}
```
- **Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "johndoe@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

### 1.2 Login (JWT)
- **Path:** `POST /api/accounts/login/`
- **Auth:** Public
- **Payload:**
```json
{
  "username": "johndoe",
  "password": "StrongPassword123!"
}
```
- **Response:**
```json
{
  "refresh": "<refresh_token>",
  "access": "<access_token>"
}
```

### 1.3 Refresh JWT
- **Path:** `POST /api/accounts/token/refresh/`
- **Auth:** Public
- **Payload:**
```json
{
  "refresh": "<refresh_token>"
}
```
- **Response:**
```json
{
  "access": "<new_access_token>"
}
```

### 1.4 Current User Profile
- **Path:** `GET /api/accounts/me/`
- **Auth:** Authenticated user(`Bearer  {Access Token}`)
- **Response:**
```json
{
  "id": 1,
  "username": "johndoe",
  "email": "johndoe@example.com",
  "first_name": "John",
  "last_name": "Doe"
}
```

- **Update profile (PUT/PATCH)**
**Payload (example):**
```json
{
  "first_name": "Johnny",
  "last_name": "Doer"
}
```
- **Response:** updated user object

### 1.5 Promote User to Superuser
- **Path:** `POST /api/accounts/<user_id>/promote/`
- **Auth:** Admin (`is_staff=True`)(`Bearer  {Access Token}`)
- **Payload:** none
- **Response:**
```json
{
  "status": "User johndoe promoted to superuser."
}
```

### 1.6 List All Users
- **Path:** `GET /api/accounts/`
- **Auth:** Admin(`Bearer  {Access Token}`)
- **Response:**
```json
[
  {
    "id": 1,
    "username": "johndoe",
    "email": "johndoe@example.com",
    "first_name": "John",
    "last_name": "Doe"
  },
  {
    "id": 2,
    "username": "alice",
    "email": "alice@example.com",
    "first_name": "Alice",
    "last_name": "Wonderland"
  }
]
```

---

## 2. Features

### 2.1 List Features
- **Path:** `GET /api/subscriptions/features/`
- **Auth:** Any authenticated user(`Bearer  {Access Token}`)
- **Response:**
```json
[
  {"id": 1, "name": "Unlimited Storage"},
  {"id": 2, "name": "Custom Reports"}
]
```

### 2.2 Create Feature
- **Path:** `POST /api/subscriptions/features/`
- **Auth:** Admin only(`Bearer  {Access Token}`)
- **Payload:**
```json
{
  "name": "Priority Support"
}
```
- **Response:**
```json
{
  "id": 3,
  "name": "Priority Support"
}
```

### 2.3 Delete Feature
- **Path:** `DELETE /api/subscriptions/features/<id>/`
- **Auth:** Admin only(`Bearer  {Access Token}`)
- **Response:** `204 No Content`

---

## 3. Plans

### 3.1 List Plans
- **Path:** `GET /api/subscriptions/plans/`
- **Auth:** Any authenticated user(`Bearer  {Access Token}`)
- **Response:**
```json
[
  {
    "id": 1,
    "name": "Pro Plan",
    "features": [
      {"id": 1, "name": "Unlimited Storage"},
      {"id": 2, "name": "Custom Reports"}
    ]
  }
]
```

### 3.2 Create Plan
- **Path:** `POST /api/subscriptions/plans/`
- **Auth:** Admin only(`Bearer  {Access Token}`)
- **Payload:**
```json
{
  "name": "Pro Plan",
  "feature_ids": [1, 2]
}
```
- **Response:**
```json
{
  "id": 1,
  "name": "Pro Plan",
  "features": [
    {"id": 1, "name": "Unlimited Storage"},
    {"id": 2, "name": "Custom Reports"}
  ]
}
```

### 3.3 Delete Plan
- **Path:** `DELETE /api/subscriptions/plans/<id>/`
- **Auth:** Admin only(`Bearer  {Access Token}`)
- **Response:** `204 No Content`

---

## 4. Subscriptions

### 4.1 List User Subscriptions
- **Path:** `GET /api/subscriptions/subscriptions/`
- **Auth:** Authenticated user(`Bearer  {Access Token}`)
- **Response:**
```json
[
  {
    "id": 1,
    "plan": {
      "id": 1,
      "name": "Pro Plan",
      "features": [
        {"id": 1, "name": "Unlimited Storage"},
        {"id": 2, "name": "Custom Reports"}
      ]
    },
    "start_date": "2025-08-29T15:30:00Z",
    "is_active": true
  }
]
```

### 4.2 Create Subscription
- **Path:** `POST /api/subscriptions/subscriptions/`
- **Auth:** Authenticated user(`Bearer  {Access Token}`)
- **Payload:**
```json
{
  "plan_id": 1
}
```
- **Response:** subscription object with nested plan

### 4.3 Change Plan
- **Path:** `POST /api/subscriptions/subscriptions/<id>/change-plan/`
- **Auth:** Owner of subscription(`Bearer  {Access Token}`)
- **Payload:**
```json
{
  "plan_id": 2
}
```
- **Response:** updated subscription with new plan

### 4.4 Deactivate Subscription
- **Path:** `POST /api/subscriptions/subscriptions/<id>/deactivate/`
- **Auth:** Owner of subscription(`Bearer  {Access Token}`)
- **Payload:** none
- **Response:**
```json
{
  "status": "subscription deactivated"
}
```

### 4.5 Delete Subscription
- **Path:** `DELETE /api/subscriptions/subscriptions/<id>/`
- **Auth:** Owner or admin(`Bearer  {Access Token}`)
- **Response:** `204 No Content`

---

### Permissions Summary

| Endpoint | Auth | Who can perform |
|----------|------|----------------|
| `/accounts/` (POST) | None | Public registration |
| `/accounts/me/` | JWT | Authenticated user |
| `/accounts/<id>/promote/` | JWT | Admin only |
| `/subscriptions/features/` (POST/DELETE) | JWT | Admin only |
| `/subscriptions/plans/` (POST/DELETE) | JWT | Admin only |
| `/subscriptions/subscriptions/` | JWT | Owner or authenticated user |
| `/subscriptions/subscriptions/<id>/change-plan/` | JWT | Owner only |
| `/subscriptions/subscriptions/<id>/deactivate/` | JWT | Owner only |

