from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    students = models.ManyToManyField(User, related_name='product_students', default=None)

class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    link_to_video = models.URLField(max_length=500)

class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    students = models.ManyToManyField(User, related_name='product_groups')
    min_users = models.PositiveIntegerField(default=0)
    max_users = models.PositiveIntegerField(default=0)

    def clean(self):
        if self.min_users > self.max_users:
            raise ValidationError("Min users cannot be greater than max users.")

