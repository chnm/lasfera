# Generated by Django 5.0.2 on 2024-11-21 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("textannotation", "0002_alter_textannotation_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="textannotation",
            name="annotation_type",
            field=models.CharField(
                choices=[
                    ("note", "Editorial Note"),
                    ("variant", "Textual Variant"),
                    ("reference", "Cross Reference"),
                ],
                default="note",
                max_length=20,
            ),
        ),
    ]
