

from utils import setup_django
setup_django()
from attendance_app.models import Student, AttendanceRecord, CustomUser
from django.contrib.auth import get_user_model
import streamlit as st
import datetime



def mark_attendance():
    st.header("✏️ Mark Attendance")
    today = st.date_input("Date", datetime.date.today())
    students = Student.objects.all()
    user_model = get_user_model()
    current_user = user_model.objects.get(username=st.session_state.user)

    for student in students:
        col1, col2 = st.columns([3,1])
        col1.write(f"{student.name} ({student.roll_number})")
        status = col2.radio(
            "", ["Present", "Absent"],
            key=f"status_{student.id}", horizontal=True
        )

        if st.button("Save", key=f"save_{student.id}"):
            AttendanceRecord.objects.update_or_create(
                student=student,
                date=today,
                defaults={"status": status, "marked_by": current_user}
            )
            st.success(f"Saved {status} for {student.name}")
