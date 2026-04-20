Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement role-based permissions across the app.

Roles:
- viewer
- coordinator
- admin

Requirements:
- viewer:
  - can log in
  - can view map
  - can view facilities list
  - can view details
- coordinator:
  - everything viewer can do
  - can create and edit facilities
- admin:
  - everything coordinator can do
  - can manage users in /admin
  - can delete facilities

Tasks:
- create reusable permission helpers or mixins
- protect views appropriately
- hide or disable UI actions based on role
- keep the implementation simple and explicit

After finishing:
- summarize permission rules and protected routes