# Generated by Django 5.0.2 on 2024-08-20 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0095_remove_location_line_code_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="linecode",
            name="associated_folio",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="manuscript.folio",
            ),
        ),
    ]
