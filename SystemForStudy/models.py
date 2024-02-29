from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    start_time = models.DateTimeField()
    price = models.IntegerField(default=0)

class Lesson(models.Model):
    name = models.CharField(max_length=200)
    link_to_video = models.URLField(max_length=500)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

class Group(models.Model):
    name = models.CharField(max_length=200)
    min_students = models.IntegerField(default=0)
    max_students = models.IntegerField(default=0)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
class User(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=50)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    product = models.ManyToManyField(Product)

