# Generated by Django 3.0.4 on 2020-03-16 21:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0013_auto_20200316_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighborhood',
            name='photo_attribution',
            field=models.TextField(blank=True, null=True),
        ),
    ]
