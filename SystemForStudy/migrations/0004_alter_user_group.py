# Generated by Django 5.0.2 on 2024-02-29 06:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemForStudy', '0003_remove_group_students_user_group'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemForStudy.group'),
        ),
    ]
