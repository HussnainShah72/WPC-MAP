import os
import sys
import django
import openpyxl

# Setup Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wpc_map.settings")
django.setup()

from facilities.models import Facility, Program
from core.wa_suburbs import WA_SUBURB_COORDINATES

# On Render, the file will be in the root folder
EXCEL_PATH = "Work Placement Host Orgnisations - Master.xlsx"

def get_coords(suburb):
    s = str(suburb or "").strip()
    for key, coords in WA_SUBURB_COORDINATES.items():
        if key.lower() == s.lower():
            return coords["latitude"], coords["longitude"]
    return None, None

def clean(val):
    if val is None:
        return ""
    return str(val).strip()

def infer_status(comments, additional):
    text = (clean(comments) + " " + clean(additional)).lower()
    if any(w in text for w in ["active", "confirmed", "approved", "accepted", "ongoing"]):
        return "active_placements"
    if any(w in text for w in ["not available", "no capacity"]):
        return "not_available"
    return "potential"

print("Starting import from Excel...")
wb = openpyxl.load_workbook(EXCEL_PATH, read_only=True, data_only=True)
ws = wb["Individual Support "]

program, _ = Program.objects.get_or_create(name="Individual Support")

count = 0
for row in ws.iter_rows(min_row=2, values_only=True):
    name = clean(row[0])
    if not name: continue
    
    suburb = clean(row[1])
    lat, lon = get_coords(suburb)
    
    # Truncate to 120 chars to fit database limits
    name_truncated = name[:120]
    suburb_truncated = suburb[:120]
    
    facility, created = Facility.objects.get_or_create(
        name=name_truncated,
        suburb=suburb_truncated,
        defaults={
            "facility_type": "aged_care",
            "latitude": lat,
            "longitude": lon,
            "status": infer_status(row[8], row[10]),
            "phone": (clean(row[6]) or clean(row[7]))[:20],
            "address": clean(row[5]),
            "quick_notes": f"{clean(row[8])}\n{clean(row[10])}".strip()
        }
    )
    facility.programs.add(program)
    if created:
        count += 1

print(f"Done! Successfully imported {count} facilities to the live database.")
