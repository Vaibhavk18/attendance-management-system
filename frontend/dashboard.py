# frontend/dashboard.py

from utils import setup_django
setup_django()  # must be before any Django model imports

import streamlit as st

# Import page functions
from attendance import mark_attendance
from reports import show_reports
from email_alerts import send_alerts
from admin_views import (
    student_list,
    teacher_list,
    all_attendance_records,
    monthly_reports,
    send_alerts_admin,
)

def show_dashboard():
    # Display user and role
    role = st.session_state.get("role", "UNKNOWN")
    st.sidebar.title(f"📋 Menu ({role})")

    # Choose menu items by role
    if role == "ADMIN":
        pages = [
            "Manage Students",
            "Manage Teachers",
            "All Attendance",
            "Monthly Reports",
            "Send Alerts",
            "Logout",
        ]
    else:  # TEACHER or default
        pages = [
            "Mark Attendance",
            "View Reports",
            "Send Alerts",
            "Logout",
        ]

    selection = st.sidebar.selectbox("Go to", pages)

    # Route to the correct function
    if selection == "Manage Students":
        student_list()
    elif selection == "Manage Teachers":
        teacher_list()
    elif selection == "All Attendance":
        all_attendance_records()
    elif selection == "Monthly Reports":
        # Admin uses admin_reports; teachers use shared reports
        if role == "ADMIN":
            monthly_reports()
        else:
            show_reports()
    elif selection == "Send Alerts":
        # Admin uses admin send; teachers use shared send (no-op for teachers)
        if role == "ADMIN":
            send_alerts_admin()
        else:
            send_alerts()
    elif selection == "Mark Attendance":
        mark_attendance()
    elif selection == "View Reports":
        show_reports()
    elif selection == "Logout":
        st.session_state.authenticated = False
        st.session_state.role = None
        st.session_state.user = None
        st.rerun()
