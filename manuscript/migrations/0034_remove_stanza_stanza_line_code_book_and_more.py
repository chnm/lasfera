# Generated by Django 5.0.2 on 2024-04-16 15:08

from django.db import migrations, models

import manuscript.models


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0033_alter_stanza_stanza_line_code_book_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stanza",
            name="stanza_line_code_book",
        ),
        migrations.RemoveField(
            model_name="stanza",
            name="stanza_line_code_line",
        ),
        migrations.RemoveField(
            model_name="stanza",
            name="stanza_line_code_stanza",
        ),
        migrations.AlterField(
            model_name="stanza",
            name="stanza_line_code",
            field=models.CharField(
                blank=True,
                help_text="Indicate where the folio begins. Input the range of text by book, stanza, and line number. For example: 01.01.01-01.01.07 would refer to book 1, stanza 1, line 1 to book 1, stanza 1, line 7.",
                max_length=20,
                null=True,
                validators=[manuscript.models.validate_line_number_code],
            ),
        ),
    ]
