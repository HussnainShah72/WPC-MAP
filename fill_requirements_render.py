import os
import django
import re

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wpc_map.settings")
django.setup()

from facilities.models import Facility, FacilityRequirement, Requirement, Program

# Keyword patterns for detection
REQUIREMENT_PATTERNS = {
    "Police Check": [r"police\s*check", r"police\s*clearance", r"npc\b"],
    "Working with Children Check": [r"working\s*with\s*children", r"wwc\b", r"wwcc\b"],
    "NDIS Screening": [r"ndis\s*screening", r"worker\s*screening"],
    "NDIS Orientation Module": [r"ndis\s*orientation", r"ndis\s*module"],
    "Flu Vaccination": [r"flu\s*vacc", r"influenza"],
    "COVID Vaccination": [r"covid\s*vacc", r"covid-?19"],
    "Immunisation History": [r"immunis[ae]", r"vaccination\s*history"],
    "Manual Handling Certificate": [r"manual\s*handling"],
    "Hand Hygiene Certificate": [r"hand\s*hygiene", r"infection\s*control"],
    "Statutory Declaration": [r"statutory\s*decl", r"stat\s*dec\b"],
    "Privacy Confidentiality Form": [r"confidentiality", r"privacy"],
    "ID Document": [r"photo\s*id", r"passport", r"licen[sc]e"],
    "Uniform Policy": [r"uniform\s*policy", r"dress\s*code"],
}

def detect_requirements(text):
    if not text: return []
    text_lower = text.lower()
    found = []
    for req_name, patterns in REQUIREMENT_PATTERNS.items():
        if any(re.search(p, text_lower) for p in patterns):
            found.append(req_name)
    return found

print("Matching Quick Notes to Requirements on live site...")
program = Program.objects.filter(name="Individual Support").first()

for facility in Facility.objects.all():
    detected = detect_requirements(facility.quick_notes)
    if not detected: continue
    
    print(f"Linking {len(detected)} requirements for: {facility.name}")
    for req_name in detected:
        requirement, _ = Requirement.objects.get_or_create(name=req_name)
        fr, created = FacilityRequirement.objects.get_or_create(
            facility=facility,
            requirement=requirement,
            defaults={"mandatory": True, "notes": "Imported from Excel notes"}
        )
        if program:
            fr.programs.add(program)

print("Done! All requirements are now linked.")
