# Generated by Django 5.0.2 on 2024-05-01 19:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0045_remove_stanzavariant_line_code"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stanzavariant",
            name="stanza_variation",
            field=models.TextField(
                blank=True,
                help_text="The variation in the stanza.",
                max_length=500,
                null=True,
                verbose_name="Significant Variations",
            ),
        ),
    ]