Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Scaffold the Django project for this app.

Requirements:
- Create a Django project named wpc_map
- Create apps:
  - accounts
  - facilities
  - core
- Configure templates, static files, and app registration
- Configure PostgreSQL-ready settings with environment variable support
- Add a custom User model in accounts
- Add a base authenticated layout template
- Add initial URL structure:
  - /auth/
  - /facilities/
  - /
  - /admin/ for the custom app admin panel route, without breaking Django admin if used separately
- Add requirements.txt
- Add .env.example
- Add a clean README section describing setup

Important:
- Do not build the full feature set yet
- Stop after scaffold + settings + app structure + URL wiring + custom user model skeleton

After finishing:
- run makemigrations if possible
- summarize all created files