# Generated by Django 5.0.2 on 2024-06-05 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "manuscript",
            "0072_alter_detail_distance_lines_alter_detail_is_sea_red_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="stanzavariant",
            name="stanza",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="manuscript.stanza",
            ),
        ),
    ]
