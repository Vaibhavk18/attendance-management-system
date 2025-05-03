from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import date
from django.conf import settings

# Branch/Semester/Section choices
BRANCH_CHOICES = [
    ('Mechanical Engineering', 'Mechanical Engineering'),
    ('Computer Science and Engineering','Computer Science and Engineering'),
    ('Information Science and Engineering','Information Science and Engineering'),
    ('Civil Engineering','Civil Engineering'),
    ('Electrical Engineering','Electrical Engineering'),
]
SEMESTER_CHOICES = [(f'Semester {i}', f'Semester {i}') for i in range(1,9)]
SECTION_CHOICES = [('A','A'),('B','B'),('C','C')]

class CustomUser(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'ADMIN', _('Admin')
        TEACHER = 'TEACHER', _('Teacher')

    role = models.CharField(max_length=10, choices=Roles.choices, default=Roles.TEACHER)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES, null=True, blank=True)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES, null=True, blank=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    branch = models.CharField(max_length=50, choices=BRANCH_CHOICES)
    semester = models.CharField(max_length=20, choices=SEMESTER_CHOICES)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.roll_number})"


class AttendanceRecord(models.Model):
    class Status(models.TextChoices):
        PRESENT = 'Present'
        ABSENT = 'Absent'

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=date.today)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PRESENT)
    marked_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('student', 'date')

    def __str__(self):
        return f"{self.student.name} - {self.date} - {self.status}"
