# Generated by Django 5.0.2 on 2024-04-16 15:12

import prose.fields
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0034_remove_stanza_stanza_line_code_book_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="folio",
            name="folio_notes",
            field=prose.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="stanza",
            name="stanza_notes",
            field=prose.fields.RichTextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="stanza",
            name="stanza_text",
            field=prose.fields.RichTextField(blank=True, null=True),
        ),
    ]