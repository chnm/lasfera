# Generated by Django 5.0.2 on 2024-02-21 20:17

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manuscript", "0008_detail_manuscript_alter_folio_iiif_url_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="singlemanuscript",
            name="manuscript_details",
        ),
        migrations.RemoveField(
            model_name="singlemanuscript",
            name="reference",
        ),
        migrations.RemoveField(
            model_name="singlemanuscript",
            name="text_decorations",
        ),
        migrations.AddField(
            model_name="reference",
            name="manuscript",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="manuscript.singlemanuscript",
            ),
        ),
        migrations.AddField(
            model_name="textdecoration",
            name="manuscript",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.PROTECT,
                to="manuscript.singlemanuscript",
            ),
        ),
    ]