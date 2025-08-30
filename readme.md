# 📦 Subscription Service & User Management (Django + DRF)

A Django REST Framework project for managing **users, features, plans, and subscriptions** with **JWT authentication**.

---

## 🔧 Requirements

- Python 3.10+  
- pip  
- Git  
- (Optional) [Postman](https://www.postman.com/) or `curl` for API testing  

> 📝 This project uses **SQLite3**, which comes built-in with Python, so no extra DB setup is needed.

---

## ⚡ Setup Guide

### 1. Clone the Repository
```bash
git clone <your-repo-url>
cd subscription_service
```

### 2. Create Virtual Environment
```bash
python -m venv env
```
Activate it:  
- Windows (PowerShell):
  ```bash
  .\env\Scripts\Activate
  ```
- Linux/Mac:
  ```bash
  source env/bin/activate
  ```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🗄 Database Setup

1. Run migrations (with reset script):  
in windows
   ```powershell
   ./reset_db.ps1
   ```
in linux
   ```shell
   ./reset_db.sh
   ```
   > (This script likely clears `db.sqlite3`, runs `makemigrations`, and `migrate`)

2. Create a superuser (admin):  
   ```bash
   python manage.py createsuperuser
   ```
   Fill in username, email, and password and also take notes of username and password
   which later will be used for creating plans, features

---

## 🚀 Running the Server
```bash
python manage.py runserver
```

Server will start at:  
👉 http://127.0.0.1:8000/

---

## 👤 User & Subscription Flow

1. **Register a new user** (`POST /api/accounts/`)  
2. **Login to get JWT tokens** (`POST /api/accounts/login/`)  
3. Use the **access token** in headers:  
   ```
   Authorization: Bearer <access_token>
   ```
4. **Admins** can create features/plans.  
5. **Users** can subscribe to a plan (`POST /api/subscriptions/subscriptions/`).  
6. Users can **change plans, deactivate, or delete subscriptions**.

---

## 🧪 Running Tests
Run the full test suite:
```bash
python manage.py test
```

---

## 📖 API Documentation

> Base URL: `/api/`  
> Auth: **JWT Bearer Token**  
> Header: `Authorization: Bearer <access_token>`

Full API reference is below:

<details>
<summary>📑 User Management</summary>

- Register → `POST /api/accounts/`  
- Login → `POST /api/accounts/login/`  
- Refresh token → `POST /api/accounts/token/refresh/`  
- Current profile → `GET /api/accounts/me/`  
- Promote to superuser → `POST /api/accounts/<id>/promote/`  
- List users (admin) → `GET /api/accounts/`  

</details>

<details>
<summary>✨ Features</summary>

- List features → `GET /api/subscriptions/features/`  
- Create feature (admin) → `POST /api/subscriptions/features/`  
- Delete feature (admin) → `DELETE /api/subscriptions/features/<id>/`  

</details>

<details>
<summary>📋 Plans</summary>

- List plans → `GET /api/subscriptions/plans/`  
- Create plan (admin) → `POST /api/subscriptions/plans/`  
- Delete plan (admin) → `DELETE /api/subscriptions/plans/<id>/`  

</details>

<details>
<summary>📦 Subscriptions</summary>

- List subscriptions → `GET /api/subscriptions/subscriptions/`  
- Create subscription → `POST /api/subscriptions/subscriptions/`  
- Change plan → `POST /api/subscriptions/subscriptions/<id>/change-plan/`  
- Deactivate subscription → `POST /api/subscriptions/subscriptions/<id>/deactivate/`  
- Delete subscription → `DELETE /api/subscriptions/subscriptions/<id>/`  

</details>

---

## 🔐 Permissions Summary

| Endpoint | Who can access |
|----------|----------------|
| `/accounts/` (register) | Public |
| `/accounts/me/` | Logged-in user |
| `/accounts/<id>/promote/` | Admin only |
| `/subscriptions/features/` (POST/DELETE) | Admin only |
| `/subscriptions/plans/` (POST/DELETE) | Admin only |
| `/subscriptions/subscriptions/` | Authenticated user |
| `/subscriptions/subscriptions/<id>/change-plan/` | Owner only |
| `/subscriptions/subscriptions/<id>/deactivate/` | Owner only |

---
there is a seperate dedicated document for provider API endpoints `api_documentation.md`

✅ With this README, your project will look professional and easy to set up!









folder-structure ->

project/
    - accounts/
        - migrations/
        - models/
            - __init__.py
            - user.py
        - serializers/
            - __init__.py
            - user.py
        - tests/
            - __init__.py
            - conftest.py
            - test_accounts.py
            - test_models.py
        - views/
            - __init__.py
            - user.py

        - __init__.py
        - admin.py
        - apps.py 
        - urls.py

    - config/
        - __init__.py
        - asgi.py
        - settings.py 
        - urls.py 
        - wsgi.py 

    - env/
    - subscriptions/
        - migrations/
        - fixtures/
            - initial_data.json
        - models/
            - base.py
            - feature.py
            - plan.py
            - subscription.py 
        - scripts/
            - load_fixtures.py
        - selectors/
            - __init__.py
            - subscription.py
        - serializers/
            - __init__.py
            - feature.py
            - plan.py
            - subscription.py
        - services/
            - __init__.py
            - subscription.py
        - views/
            - __init__.py
            - plan.py
            - subscription.py
        - tests/
            - __init__.py
            - conftest.py
            - test_models.py
            - test_plans.py
            - test_subscriptions_api.py

        - __init__.py
        - admin.py
        - apps.py
        - urls.py

    .env.example
    db.sqlite3
    manage.py
    requirements.txt
    reset_db.ps1
    reset_db.sh


    


