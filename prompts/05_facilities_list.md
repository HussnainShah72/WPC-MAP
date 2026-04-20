Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement the Facilities list page at /facilities.

Requirements:
- authenticated access
- page header and nav consistent with the app
- controls:
  - search field with placeholder "Search facilities..."
  - status dropdown
  - type dropdown
  - Add facility button
- table columns:
  - checkbox
  - Name
  - Type
  - Suburb
  - Programs
  - Status
  - Spots
  - Next start
  - Actions
- sortable columns:
  - Name
  - Type
  - Suburb
- actions menu per row:
  - Edit
  - Delete

Filtering:
- keyword search
- filter by status
- filter by type

Display:
- show program badges
- show status badges
- show spots as number badges
- next start may be blank/dash

Behavior:
- clicking a facility row should open a reusable right-side detail panel
- clicking the Actions menu should not open the row panel

Implementation notes:
- use Django templates
- GET-based filters and sorting are acceptable
- keep code simple and maintainable

After finishing:
- summarize views, forms, templates, and query logic