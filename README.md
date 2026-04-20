# Workplacement Map

Internal Django application for placement facility discovery and management.

## Main modules
- Accounts and restricted signup
- Admin user access management
- Facilities list and facility CRUD
- Map-based facility discovery
- Facility side panel and full details modal

## Roles
- viewer
- coordinator
- admin

## Core routes
- /auth/login
- /auth/sign-up
- /auth/forgot-password
- /
- /facilities
- /facilities/new
- /facilities/<id>/edit
- /admin

## Stack
- Django
- PostgreSQL-ready configuration
- Django templates
- Leaflet + OpenStreetMap
- HTML/CSS/JS

## Setup
1. Create and activate a virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env` and update values as needed.
4. Run migrations with `python manage.py migrate`.
5. Create a superuser with `python manage.py createsuperuser`.
6. Start the app with `python manage.py runserver`.

## Routes
- App home map: `/`
- Auth: `/auth/login/`, `/auth/sign-up/`, `/auth/forgot-password/`
- Facilities: `/facilities/`, `/facilities/new/`, `/facilities/<id>/edit/`, `/facilities/<id>/delete/`
- Custom app admin: `/admin/`
- Django admin: `/django-admin/`

## Environment notes
- Local development defaults to SQLite if `DATABASE_URL` is empty.
- Set `DATABASE_URL` to a PostgreSQL connection string when you want PostgreSQL.
- The project uses a custom `accounts.User` model with email as the login identifier.
