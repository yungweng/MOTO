# Generated by Django 4.2.5 on 2024-11-06 21:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_device_delete_authtoken'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='device_id',
            field=models.CharField(max_length=255),
        ),
    ]
