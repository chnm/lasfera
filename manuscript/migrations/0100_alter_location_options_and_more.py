# Generated by Django 5.0.2 on 2024-09-09 13:59

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0099_alter_location_country"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="location",
            options={
                "ordering": ["placename_id"],
                "verbose_name": "Toponym",
                "verbose_name_plural": "Toponyms",
            },
        ),
        migrations.AlterUniqueTogether(
            name="location",
            unique_together={("placename_id",)},
        ),
        migrations.RemoveField(
            model_name="location",
            name="country",
        ),
    ]