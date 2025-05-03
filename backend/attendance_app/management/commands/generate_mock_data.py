# backend/attendance_app/management/commands/generate_mock_data.py

import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from attendance_app.models import Student, BRANCH_CHOICES, SEMESTER_CHOICES, SECTION_CHOICES
from faker import Faker

User = get_user_model()
fake = Faker()

class Command(BaseCommand):
    help = "Generate mock data: 300 students, 50 teachers"

    def handle(self, *args, **options):
        # Clear existing mock data (optional)
        Student.objects.all().delete()
        User.objects.filter(role=User.Roles.TEACHER).delete()
        
        branches = [b for b,_ in BRANCH_CHOICES]
        semesters = [s for s,_ in SEMESTER_CHOICES]
        sections = [sec for sec,_ in SECTION_CHOICES]

        # Generate students
        total_students = 300
        self.stdout.write("Creating 300 students...")
        for i in range(1, total_students+1):
            name = fake.name()
            roll = f"{random.choice(branches)[:3].upper()}{random.choice(semesters).split()[1]}{random.choice(sections)}{i:03d}"
            email = f"{name.replace(' ', '.').lower()}{i}@example.com"
            branch = branches[(i-1) % len(branches)]
            semester = semesters[(i-1) % len(semesters)]
            section = sections[(i-1) % len(sections)]
            Student.objects.create(
                name=name,
                roll_number=roll,
                email=email,
                branch=branch,
                semester=semester,
                section=section
            )
        self.stdout.write(self.style.SUCCESS("✅ 300 students created."))

        # Generate teachers
        total_teachers = 50
        self.stdout.write("Creating 50 teachers...")
        for i in range(1, total_teachers+1):
            username = fake.user_name() + str(i)
            email = f"{username}@school.com"
            password = "Teach@123"  # you can change this
            branch = random.choice(branches)
            semester = random.choice(semesters)
            section = random.choice(sections)
            User.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=User.Roles.TEACHER,
                branch=branch,
                semester=semester,
                section=section
            )
        self.stdout.write(self.style.SUCCESS("✅ 50 teachers created."))

        self.stdout.write(self.style.SUCCESS("🎉 Mock data generation complete."))
