# Generated manually because Django is not runnable in this environment.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("facilities", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="facility",
            name="aha_current_students",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="aha_last_placement",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="aha_next_start",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="aha_spots_available",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="is_current_students",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="is_last_placement",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="is_next_start",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="facility",
            name="is_spots_available",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
