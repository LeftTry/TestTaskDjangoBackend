# Generated by Django 5.0.2 on 2024-03-01 09:39

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SystemForStudy', '0006_alter_group_product_alter_group_students_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='students',
            field=models.ManyToManyField(default=None, null=True, related_name='product_students', to=settings.AUTH_USER_MODEL),
        ),
    ]
