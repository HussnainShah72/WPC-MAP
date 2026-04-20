Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement facility create and edit pages.

Routes:
- /facilities/new
- /facilities/<id>/edit

Use one reusable form page/template for create and edit.

Page sections:
1. Identity
2. Placement
3. Schedule
4. Compliance
5. Geo
6. People & Admin

Identity fields:
- Facility name
- Type
- Address
- Postcode
- Suburb
- State
- Website
- Phone
- Quick notes

Facility type choices:
- Aged Care
- Allied Health
- Hospital
- Clinic
- Rehabilitation
- Pharmacy
- Physiotherapy
- Other

Placement fields:
- Status
- Accepts students
- Program acceptance toggles for:
  - IS
  - AHA

Status choices:
- Active placements
- Upcoming placements
- Previous placements
- Potential
- Not available

Schedule fields:
- Orientation time
- Start time day 1
- Dynamic shifts list
- Add shift button

Compliance fields:
- Orientation required
- Uniform policy
- Parking info
- Dynamic requirements list
- Add requirement button

Geo fields:
- Raw coordinates
- Latitude
- Longitude
- Accuracy
- Verified

People & Admin fields:
- MOU complete
- Contacted recently
- Dynamic contacts list
- Add contact button

Requirements:
- use Django ModelForms and formsets or inline formsets
- create/edit must save parent and child records correctly
- include Cancel and Save buttons
- create clean validation where appropriate
- create and edit should be coordinator/admin only

After finishing:
- summarize form architecture and any assumptions