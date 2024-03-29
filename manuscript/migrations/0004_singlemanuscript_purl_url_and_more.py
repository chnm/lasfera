# Generated by Django 5.0.2 on 2024-02-21 19:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manuscript", "0003_alter_page_stanzas_alter_stanza_locations_mentioned"),
    ]

    operations = [
        migrations.AddField(
            model_name="singlemanuscript",
            name="purl_url",
            field=models.URLField(
                blank=True,
                help_text="The URL to the permanent URL for the manuscript. If there isn't one, leave blank.",
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="singlemanuscript",
            name="manuscript_destroyed",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AlterField(
            model_name="singlemanuscript",
            name="manuscript_lost",
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.CreateModel(
            name="Folio",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("page_number", models.IntegerField(blank=True, null=True)),
                ("page_notes", models.TextField(blank=True, null=True)),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        help_text="The image of the page from the manuscript.",
                        null=True,
                        upload_to="",
                    ),
                ),
                (
                    "iiif_url",
                    models.URLField(
                        blank=True,
                        help_text="Provide a IIIF manifest to a page in the manuscript. If there isn't one, leave blank.",
                        null=True,
                    ),
                ),
                (
                    "manuscript",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="manuscript.singlemanuscript",
                    ),
                ),
                ("stanzas", models.ManyToManyField(blank=True, to="manuscript.stanza")),
            ],
        ),
        migrations.DeleteModel(
            name="Page",
        ),
    ]
