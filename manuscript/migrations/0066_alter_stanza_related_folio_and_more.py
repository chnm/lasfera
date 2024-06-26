# Generated by Django 5.0.2 on 2024-05-22 15:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "manuscript",
            "0065_alter_library_options_alter_singlemanuscript_options_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="stanza",
            name="related_folio",
            field=models.ForeignKey(
                blank=True,
                help_text="Optional. The folio to which the stanza belongs.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="manuscript.folio",
            ),
        ),
        migrations.AlterField(
            model_name="stanza",
            name="related_manuscript",
            field=models.ForeignKey(
                help_text="Required. The manuscript to which the stanza belongs.",
                on_delete=django.db.models.deletion.CASCADE,
                to="manuscript.singlemanuscript",
            ),
        ),
    ]
