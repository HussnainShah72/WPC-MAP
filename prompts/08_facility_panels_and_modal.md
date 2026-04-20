Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement reusable facility detail UI components:
1. right-side detail panel
2. full details modal

These components must work from:
- map marker click
- facilities row click

Right-side detail panel should show:
- facility name
- type badge
- status badge
- program acceptance
- address
- phone
- website
- quick notes
- selected summary fields
- action buttons:
  - Directions
  - Call Now
  - Email Contact
  - Website
  - See details
  - Edit
  - Delete

Full details modal should show sections:
- Overview
- Compliance requirements
- Placement
- Placement Schedule
- Shifts
- Contacts

Requirements:
- make these components reusable
- create a clean endpoint or partial-loading strategy
- do not duplicate large amounts of template code
- support facility display from both map and facilities table

After finishing:
- summarize partials/components and how they are loaded