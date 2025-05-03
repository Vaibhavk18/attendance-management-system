

from utils import setup_django
setup_django()
from attendance_app.views import send_low_attendance_alerts
import streamlit as st



def send_alerts():
    st.header("✉️ Send Low Attendance Alerts")
    if st.button("Send Alerts Now"):
        emails = send_low_attendance_alerts()
        if emails:
            st.success(f"Alerts sent to: {', '.join(emails)}")
        else:
            st.info("No students below threshold.")
