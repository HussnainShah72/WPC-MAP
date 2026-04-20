Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement the full Django data model for the app.

Accounts models:
1. User
   - email login
   - role choices: viewer, coordinator, admin
   - is_active
   - is_staff
   - date_joined

2. AllowedSignupEmail
   - email
   - role
   - is_registered
   - created_at

Facilities models:
1. Program
   - name
   - seed with AHA and IS later

2. Facility
   - name
   - facility_type
   - address
   - suburb
   - postcode
   - state
   - website
   - phone
   - quick_notes
   - status
   - accepts_students
   - orientation_required
   - uniform_policy
   - parking_info
   - orientation_time
   - start_time_day1
   - mou_complete
   - contacted_recently
   - spots
   - next_start
   - geo_raw
   - latitude
   - longitude
   - geo_accuracy
   - geo_verified
   - many-to-many programs
   - created_at
   - updated_at

3. Requirement
   - name

4. FacilityRequirement
   - facility
   - requirement
   - mandatory
   - program

5. FacilityShift
   - facility
   - role/program
   - days
   - time_range
   - notes

6. FacilityContact
   - facility
   - role
   - name
   - email
   - phone
   - many-to-many programs

Requirements:
- Use clear choices for facility type and facility status
- Add __str__ methods
- Add sensible related_name values
- Create migrations
- Register models in Django admin if easy

After finishing:
- run makemigrations
- summarize models and migrations