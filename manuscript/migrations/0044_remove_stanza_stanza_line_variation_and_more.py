# Generated by Django 5.0.2 on 2024-04-25 17:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0043_stanzavariant_variation_type_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stanza",
            name="stanza_line_variation",
        ),
        migrations.AddField(
            model_name="stanzavariant",
            name="stanza",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="manuscript.stanza",
            ),
        ),
        migrations.AlterField(
            model_name="stanzavariant",
            name="stanza_variation",
            field=models.TextField(
                blank=True,
                help_text="The variation in the stanza.",
                max_length=255,
                null=True,
                verbose_name="Significant Variations",
            ),
        ),
    ]