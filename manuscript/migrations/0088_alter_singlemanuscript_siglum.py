# Generated by Django 5.0.2 on 2024-07-25 13:24

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("manuscript", "0087_singlemanuscript_photographs"),
    ]

    operations = [
        migrations.AlterField(
            model_name="singlemanuscript",
            name="siglum",
            field=models.CharField(
                blank=True, db_index=True, max_length=20, null=True, unique=True
            ),
        ),
    ]
