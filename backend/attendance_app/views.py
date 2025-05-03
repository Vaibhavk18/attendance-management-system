from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .forms import CustomUserSignupForm, CustomLoginForm, StudentForm, AttendanceForm,TeacherCreationForm
from .models import Student, AttendanceRecord
from datetime import date
from django.contrib import messages
from django.db.models import Count,Q
from .models import AttendanceRecord, Student,CustomUser
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from collections import defaultdict

def signup(request):
    if request.method == 'POST':
        form = CustomUserSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomUserSignupForm()
    return render(request, 'signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = CustomLoginForm()
    return render(request, 'login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    return render(request, 'dashboard.html')


@login_required
def student_list(request):
    students = Student.objects.all()
    return render(request, 'student_list.html', {'students': students})


@login_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'add_student.html', {'form': form})


@login_required
def mark_attendance(request):
    students = Student.objects.all()
    if request.method == 'POST':
        for student in students:
            status = request.POST.get(f'status_{student.id}')
            if status:
                AttendanceRecord.objects.update_or_create(
                    student=student,
                    date=date.today(),
                    defaults={'status': status, 'marked_by': request.user}
                )
        messages.success(request, "Attendance marked successfully.")
        return redirect('mark_attendance')
    return render(request, 'mark_attendance.html', {'students': students})


@login_required
def attendance_report(request):
    data = AttendanceRecord.objects.values('student__name').annotate(
        present_count=Count('id', filter=Q(status='Present')),
        absent_count=Count('id', filter=Q(status='Absent'))
    )
    return render(request, 'attendance_report.html', {'data': data})






def monthly_attendance_report(request):
    students = Student.objects.all()
    report_data = []

    for student in students:
        records = AttendanceRecord.objects.filter(student=student)
        monthly_data = defaultdict(lambda: {'present': 0, 'absent': 0})

        for record in records:
            month = record.date.strftime("%Y-%m")
            if record.status == 'Present':
                monthly_data[month]['present'] += 1
            else:
                monthly_data[month]['absent'] += 1

        student_data = {
            'name': student.name,
            'roll_number': student.roll_number,
            'monthly_attendance': []
        }

        for month, counts in sorted(monthly_data.items()):
            total = counts['present'] + counts['absent']
            percentage = (counts['present'] / total) * 100 if total > 0 else 0
            student_data['monthly_attendance'].append({
                'month': month,
                'present': counts['present'],
                'absent': counts['absent'],
                'percentage': round(percentage, 2)
            })

        report_data.append(student_data)

    context = {
        'report_data': report_data
    }

    return render(request, 'attendance_app/monthly_report.html', context)




def graph_data_api(request):
    students = Student.objects.all()
    bar_data = []
    pie_data = {'Present': 0, 'Absent': 0}

    for student in students:
        records = AttendanceRecord.objects.filter(student=student)
        present_count = records.filter(status='Present').count()
        absent_count = records.filter(status='Absent').count()

        # Bar chart data
        bar_data.append({
            'name': student.name,
            'present': present_count,
            'absent': absent_count,
        })

        # Pie chart data (aggregate)
        pie_data['Present'] += present_count
        pie_data['Absent'] += absent_count

    return JsonResponse({
        'bar_chart': bar_data,
        'pie_chart': pie_data,
    })

# attendance_app/utils.py


def send_low_attendance_alerts(threshold=75):
    from .models import Student, AttendanceRecord
    from collections import defaultdict

    alerts_sent = []

    for student in Student.objects.all():
        records = AttendanceRecord.objects.filter(student=student)
        present = records.filter(status='Present').count()
        total = records.count()

        if total == 0:
            continue

        percentage = (present / total) * 100

        if percentage < threshold:
            send_mail(
                subject='⚠ Low Attendance Alert',
                message=f"Dear {student.name},\n\nYour attendance is {percentage:.2f}%. Please maintain above 75%.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student.email],
                fail_silently=False,
            )
            alerts_sent.append(student.email)

    return alerts_sent


from .models import Student
from .forms import StudentForm
from .decorator import role_required

@role_required('Admin')
def student_list(request):
    students = Student.objects.all()
    return render(request, 'attendance_app/admin/student_list.html', {'students': students})

@role_required('Admin')
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm()
    return render(request, 'attendance_app/admin/add_student.html', {'form': form})

@role_required('Admin')
def edit_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    if request.method == 'POST':
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
    else:
        form = StudentForm(instance=student)
    return render(request, 'attendance_app/admin/edit_student.html', {'form': form})

@role_required('Admin')
def delete_student(request, student_id):
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    return redirect('student_list')

@role_required('Admin')
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('teacher_list')
    else:
        form = TeacherCreationForm(initial={'role': 'Teacher'})
    return render(request, 'attendance_app/admin/create_teacher.html', {'form': form})

@role_required('Admin')
def teacher_list(request):
    teachers = CustomUser.objects.filter(role='Teacher')
    return render(request, 'attendance_app/admin/teacher_list.html', {'teachers': teachers})

@role_required('Admin')
def all_attendance_records(request):
    records = AttendanceRecord.objects.select_related('student').order_by('-date')
    return render(request, 'attendance_app/admin/all_attendance.html', {'records': records})

from .utils import generate_monthly_report
def view_monthly_report(request):
    report_data = generate_monthly_report()
    return render(request, 'attendance_app/admin/monthly_report.html', {'report_data': report_data})






