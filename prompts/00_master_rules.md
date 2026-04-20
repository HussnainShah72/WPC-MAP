You are building a production-style Django application in this repository.

Project goals:
- Clone an internal placement facility management app
- Use Django with server-rendered templates
- Keep code clean, modular, and maintainable
- Prefer simple architecture over unnecessary abstraction

Global rules:
1. Work only inside this repository.
2. Preserve existing working code unless the task explicitly asks for refactoring.
3. Use Django best practices.
4. Use a custom User model with email login.
5. Use PostgreSQL-ready settings, but keep local development easy.
6. Use Django templates, not React.
7. Use plain JavaScript where needed.
8. Use Leaflet + OpenStreetMap for the map.
9. Keep styling clean and close to the referenced app.
10. When a task is complete:
   - summarize changed files
   - list any commands run
   - list any follow-up tasks or blockers
11. If migrations are changed, generate them.
12. If tests are practical, add or run them.
13. Do not invent business rules that conflict with SPEC.md.
14. Read README.md and SPEC.md before making changes.