# Generated by Django 5.0.2 on 2024-03-19 19:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuscript', '0015_alter_location_options_editorialstatus_iiif_url_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='textdecoration',
            name='white_vine_work',
            field=models.BooleanField(blank=True, null=True),
        ),
    ]
