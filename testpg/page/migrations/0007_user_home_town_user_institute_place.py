# Generated by Django 4.2.19 on 2025-02-26 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0006_sponsor_events_content_events_layout_events_timing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='home_town',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='institute_place',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
