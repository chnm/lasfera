# Generated by Django 5.0.2 on 2024-02-21 19:51

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("manuscript", "0005_viewernote_related_manuscript"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="viewernote",
            name="viewer",
            field=models.ForeignKey(
                blank=True,
                help_text="The user who viewed the manuscript.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="viewer",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]