from datetime import datetime
from collections import defaultdict
from .models import AttendanceRecord

def generate_monthly_report():
    """
    Returns a dictionary: 
    { 'Student Name': { '2025-05': { 'present': 20, 'absent': 5, 'percentage': 80.0 }, ... }, ... }
    """
    records = AttendanceRecord.objects.select_related('student')
    report = defaultdict(lambda: defaultdict(lambda: {'present': 0, 'absent': 0, 'percentage': 0.0}))

    for rec in records:
        student = rec.student.name
        month_key = rec.date.strftime('%Y-%m')
        status = rec.status
        if status == 'Present':
            report[student][month_key]['present'] += 1
        else:
            report[student][month_key]['absent'] += 1

    # Calculate percentage
    for student in report:
        for month in report[student]:
            present = report[student][month]['present']
            absent = report[student][month]['absent']
            total = present + absent
            percentage = (present / total) * 100 if total > 0 else 0
            report[student][month]['percentage'] = round(percentage, 2)

    return report
