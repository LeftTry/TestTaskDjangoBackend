# Generated by Django 5.0.2 on 2024-02-29 12:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemForStudy', '0005_remove_group_max_students_remove_group_min_students_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='group',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemForStudy.product'),
        ),
        migrations.AlterField(
            model_name='group',
            name='students',
            field=models.ManyToManyField(related_name='product_groups', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='lesson',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='SystemForStudy.product'),
        ),
        migrations.AlterField(
            model_name='product',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
