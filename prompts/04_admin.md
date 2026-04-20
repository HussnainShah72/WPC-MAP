Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement the custom application admin panel at /admin for user access management.

This is NOT the default Django admin interface. It is the app's own admin page.

Requirements:
- admin-only access
- page title: Admin Panel
- subtitle: Manage users and system access permissions
- show a badge with total user count
- section 1: Add New User
  - fields:
    - Email Address
    - Role dropdown
  - button:
    - Add User
- section 2: User Management
  - list current users or allowed signup entries in a clean card list
  - each row/card should show:
    - email
    - role badge
    - added date
    - edit button
    - delete button

Business logic:
- adding a user should create an AllowedSignupEmail entry if one does not exist
- role choices:
  - viewer
  - coordinator
  - admin
- editing should allow changing the role
- deleting should remove the invitation or user access record safely

Important:
- preserve the exact restricted-signup system from SPEC.md
- do not rely on Django admin UI for this page

After finishing:
- summarize route, forms, views, and templates created