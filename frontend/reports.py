

from utils import setup_django
setup_django()
import streamlit as st
import matplotlib.pyplot as plt
from attendance_app.utils import generate_monthly_report



def show_reports():
    st.header("📊 Monthly Attendance Reports")
    report = generate_monthly_report()

    student = st.selectbox("Select student", list(report.keys()))
    data = report.get(student, {})

    if not data:
        st.info("No records available.")
        return

    months = list(data.keys())
    present = [data[m]["present"] for m in months]
    absent = [data[m]["absent"] for m in months]
    pct = [data[m]["percentage"] for m in months]

    # Table
    st.write("| Month | Present | Absent | % |")
    st.write("|---|---|---|---|")
    for m in months:
        st.write(f"| {m} | {data[m]['present']} | {data[m]['absent']} | {data[m]['percentage']}% |")

    # Bar chart: present vs absent
    fig, ax = plt.subplots()
    ax.bar(months, present, label="Present")
    ax.bar(months, absent, bottom=present, label="Absent")
    ax.set_ylabel("Days")
    ax.set_title(f"Attendance for {student}")
    ax.legend()
    st.pyplot(fig)
