# Generated by Django 4.2.19 on 2025-02-27 06:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('page', '0008_remove_teammember_email_remove_teammember_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='events',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
