# Generated by Django 5.0.2 on 2024-05-30 16:43

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0070_alter_location_line_code_alter_location_placename_id"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="folio",
            options={"ordering": ["folio_number"]},
        ),
        migrations.AlterModelOptions(
            name="stanza",
            options={"ordering": ["id"]},
        ),
    ]