# Generated by Django 3.0.4 on 2020-03-16 21:26

import django.contrib.gis.db.models.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0012_place_image_attribution'),
    ]

    operations = [
        migrations.AddField(
            model_name='neighborhood',
            name='geom',
            field=django.contrib.gis.db.models.fields.PointField(null=True, srid=4326),
        ),
        migrations.AddField(
            model_name='neighborhood',
            name='lat',
            field=models.FloatField(default=10.0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='neighborhood',
            name='lng',
            field=models.FloatField(default=10.0),
            preserve_default=False,
        ),
    ]