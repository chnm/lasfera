# Generated by Django 5.0.2 on 2024-06-14 14:19

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0084_alter_location_related_folio"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="related_folio",
        ),
    ]
