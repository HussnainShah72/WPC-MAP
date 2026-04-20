Read README.md, SPEC.md, and prompts/00_master_rules.md first.

Task:
Implement the authenticated map homepage at /.

Requirements:
- split layout:
  - left filter/results sidebar
  - right interactive map
- use Leaflet with OpenStreetMap

Left sidebar:
- title: WPC Map
- filters section
- search input with placeholder: Search by anything...
- suburb input with placeholder: Search by suburb...
- radius dropdown with options:
  - All distances
  - 5 km
  - 10 km
  - 15 km
  - 20 km
  - 25 km
  - 30 km
- type dropdown
- status dropdown
- reset view control
- results count
- alphabetic sort indicator if practical
- facility results list with:
  - name
  - address
  - type badge
  - status badge

Map behavior:
- render facility markers from latitude/longitude
- color markers by status
- hover popup should show:
  - name
  - type
  - status
  - address
  - phone
  - website
  - helper text: Click marker for full details
- clicking a marker should:
  - focus/zoom map
  - open right-side detail panel

Filtering logic:
- keyword
- suburb
- radius
- type
- status

Implementation notes:
- use simple, reliable JavaScript
- if radius-by-suburb needs approximation initially, implement a clean placeholder and document it
- prioritize a working end-to-end page

After finishing:
- summarize data flow, templates, and JS behavior