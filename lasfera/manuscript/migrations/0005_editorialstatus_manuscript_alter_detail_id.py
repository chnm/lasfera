# Generated by Django 5.0 on 2024-01-24 16:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuscript', '0004_alter_singlemanuscript_library'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorialstatus',
            name='manuscript',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='manuscript.singlemanuscript'),
        ),
        migrations.AlterField(
            model_name='detail',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]