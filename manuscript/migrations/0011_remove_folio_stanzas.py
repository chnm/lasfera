# Generated by Django 5.0.2 on 2024-02-21 20:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("manuscript", "0010_stanza_related_folio"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="folio",
            name="stanzas",
        ),
    ]
