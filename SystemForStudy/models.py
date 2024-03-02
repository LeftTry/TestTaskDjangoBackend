from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, User


class Product(models.Model):
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    start_time = models.DateTimeField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    students = models.ManyToManyField(User, related_name='product_students', default=None)

    def rebuild_groups(self):
        groups = Group.objects.filter(product_id=self.id).order_by('id')
        students = self.students.all()

        min_max_students = 0
        for group in groups:
            min_max_students = max(min_max_students, int(group.max_users))

        max_min_students = 0
        for group in groups:
            min_students = max(max_min_students, int(group.min_users))

        if groups.count() == 0:
            return

        average_students = self.students.count() / groups.count()

        target_students_in_group = 0

        if average_students < min_max_students:
            if average_students < max_min_students:
                target_students_in_group = - 2
            target_students_in_group = average_students
        else:
            target_students_in_group = -1

        if self.start_time > timezone.now():
            if target_students_in_group == -1:
                i = 0
                for group in groups:
                    group.students.clear()
                    while group.students.count() < group.min_users and i < students.count():
                        group.students.add(students[i])
                        i += 1
                for group in groups:
                    group.students.clear()
                    while group.students.count() < group.max_users and i < students.count():
                        group.students.add(students[i])
                        i += 1
            elif target_students_in_group == -2:
                i = 0
                for group in groups:
                    group.students.all().delete()
                    while group.students.count() < group.min_users and i < students.count():
                        group.students.add(students[i])
                        i += 1
            else:
                i = 0
                for group in groups:
                    group.students.all().delete()
                    while group.students.count() < group.max_users and i < students.count():
                        group.students.add(students[i])
                        i += 1
                for group in groups:
                    group.students.all().delete()
                    while group.students.count() < target_students_in_group and i < students.count():
                        group.students.add(students[i])
                        i += 1


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
