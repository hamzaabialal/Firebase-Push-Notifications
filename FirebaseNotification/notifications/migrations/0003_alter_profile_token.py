# Generated by Django 4.2.9 on 2024-01-09 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0002_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='token',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
