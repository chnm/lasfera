# Generated by Django 5.0.2 on 2024-03-19 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuscript', '0018_alter_editorialstatus_collated'),
    ]

    operations = [
        migrations.AddField(
            model_name='viewernote',
            name='viewer_initials',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
