# Generated by Django 5.0.2 on 2024-06-13 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0082_remove_location_related_manuscript"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="location",
            name="related_folio",
        ),
        migrations.AddField(
            model_name="location",
            name="related_folio",
            field=models.ManyToManyField(
                blank=True,
                help_text="The folio where the toponym is mentioned.",
                null=True,
                to="manuscript.folio",
            ),
        ),
    ]