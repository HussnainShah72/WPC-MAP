# Product Spec

## Purpose
An internal application used by staff to find and manage student placement facilities.

## Authentication
### Login
- URL: /auth/login
- Fields: email, password
- Error on invalid login: "Invalid login credentials"

### Signup
- URL: /auth/sign-up
- Fields: email, password, repeat password
- Signup is restricted
- If email is not approved, show: "This email is not allowed to sign up"

### Forgot password
- URL: /auth/forgot-password
- Field: email

## Roles
- viewer
- coordinator
- admin

## Admin panel
- URL: /admin
- Add new user by email and role
- Manage users list with edit/delete
- Roles visible as badges

## Facilities list
- URL: /facilities
- Search field
- Status dropdown
- Type dropdown
- Add facility button
- Table columns:
  - Name
  - Type
  - Suburb
  - Programs
  - Status
  - Spots
  - Next start
  - Actions
- Actions menu:
  - Edit
  - Delete

## Add/Edit facility
- URL: /facilities/new
- Sections:
  - Identity
  - Placement
  - Schedule
  - Compliance
  - Geo
  - People & Admin

### Identity fields
- Facility name
- Type
- Address
- Postcode
- Suburb
- State
- Website
- Phone
- Quick notes

### Facility type options
- Aged Care
- Allied Health
- Hospital
- Clinic
- Rehabilitation
- Pharmacy
- Physiotherapy
- Other

### Placement fields
- Status
- Accepts students
- Program acceptance: IS, AHA

### Placement status options
- Active placements
- Upcoming placements
- Previous placements
- Potential
- Not available

### Schedule fields
- Orientation time
- Start time day 1
- Shifts

### Compliance fields
- Orientation required
- Uniform policy
- Parking info
- Requirements list

### Geo fields
- Raw coordinates text
- Latitude
- Longitude
- Accuracy
- Verified

### People & Admin fields
- MOU complete
- Contacted recently
- Contacts list

## Map homepage
- URL: /
- Left filter sidebar
- Right interactive map
- Search by anything
- Search by suburb
- Radius dropdown
- Type dropdown
- Status dropdown
- Results list
- Reset view
- Marker hover popup
- Marker click detail panel
- "See details" full modal

### Radius options
- All distances
- 5 km
- 10 km
- 15 km
- 20 km
- 25 km
- 30 km

### Type filter
- All types
- aged care

### Status filter
- All statuses
- Active placements
- Upcoming placements
- Previous placements
- Potential partners
- Not available

## Facility side panel
Shown from map marker click or facilities row click

### Fields shown
- Name
- Type
- Status
- Program acceptance
- Address
- Phone
- Website
- Quick notes
- Compliance summary in some contexts

### Buttons
- Directions
- Call Now
- Email Contact
- Website
- See details
- Edit
- Delete

## Full facility details modal
Sections:
- Overview
- Compliance requirements
- Placement
- Placement schedule
- Shifts
- Contacts