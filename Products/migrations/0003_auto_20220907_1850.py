# Generated by Django 3.2.15 on 2022-09-07 18:50

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Products', '0002_auto_20220907_1842'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seen',
            name='category_id_fk',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Products.category'),
        ),
        migrations.AlterField(
            model_name='seen',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 7, 18, 50, 1, 262695)),
        ),
        migrations.AlterField(
            model_name='sold',
            name='created_on',
            field=models.DateTimeField(default=datetime.datetime(2022, 9, 7, 18, 50, 1, 262695)),
        ),
    ]
