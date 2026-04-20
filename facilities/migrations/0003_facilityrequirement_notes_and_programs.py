# Generated manually because Django is not runnable in this environment.

from django.db import migrations, models


def copy_requirement_program_to_m2m(apps, schema_editor):
    FacilityRequirement = apps.get_model("facilities", "FacilityRequirement")
    for item in FacilityRequirement.objects.exclude(program__isnull=True):
        item.programs.add(item.program)


class Migration(migrations.Migration):

    dependencies = [
        ("facilities", "0002_facility_program_detail_fields"),
    ]

    operations = [
        migrations.AddField(
            model_name="facilityrequirement",
            name="notes",
            field=models.TextField(blank=True),
        ),
        migrations.AddField(
            model_name="facilityrequirement",
            name="programs",
            field=models.ManyToManyField(blank=True, related_name="facility_requirement_items", to="facilities.program"),
        ),
        migrations.RunPython(copy_requirement_program_to_m2m, migrations.RunPython.noop),
    ]
