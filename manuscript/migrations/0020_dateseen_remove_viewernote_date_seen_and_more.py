# Generated by Django 5.0.2 on 2024-03-19 19:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manuscript', '0019_viewernote_viewer_initials'),
    ]

    operations = [
        migrations.CreateModel(
            name='DateSeen',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='viewernote',
            name='date_seen',
        ),
        migrations.AddField(
            model_name='viewernote',
            name='dates_seen',
            field=models.ManyToManyField(blank=True, to='manuscript.dateseen'),
        ),
    ]