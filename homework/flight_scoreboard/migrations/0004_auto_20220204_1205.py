# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2022-02-04 09:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('flight_scoreboard', '0003_auto_20220204_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='flight',
            name='type_airplane',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='flight_scoreboard.TypeAirPlane', verbose_name='\u0442\u0438\u043f \u0441\u0430\u043c\u043e\u043b\u0435\u0442\u0430'),
        ),
    ]