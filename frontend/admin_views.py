# frontend/admin_views.py
from utils import setup_django
setup_django()

import streamlit as st
import pandas as pd
from attendance_app.models import Student, AttendanceRecord, CustomUser,BRANCH_CHOICES,SEMESTER_CHOICES,SECTION_CHOICES
from attendance_app.utils import generate_monthly_report
from attendance_app.views import send_low_attendance_alerts
import matplotlib.pyplot as plt
import datetime

def get_branches(): return [b for b,_ in BRANCH_CHOICES]
def get_semesters(): return [s for s,_ in SEMESTER_CHOICES]
def get_sections(): return [sec for sec,_ in SECTION_CHOICES]

def page_header(title, subtitle=None):
    st.markdown(f"## 📚 {title}")
    if subtitle: st.markdown(f"*{subtitle}*")
    st.markdown("---")

def apply_academic_filters(qs, key):
    branch = st.sidebar.selectbox("Branch", ["All"]+get_branches(), key=f"br_{key}")
    sem    = st.sidebar.selectbox("Semester", ["All"]+get_semesters(), key=f"sem_{key}")
    sec    = st.sidebar.selectbox("Section", ["All"]+get_sections(), key=f"sec_{key}")
    if branch!="All": qs=qs.filter(branch=branch)
    if sem!="All":    qs=qs.filter(semester=sem)
    if sec!="All":    qs=qs.filter(section=sec)
    return qs

def student_list():
    if st.session_state.role!="ADMIN": st.error("Admins only"); return
    page_header("Manage Students","Add/search/filter/export")
    with st.expander("➕ Add New Student"):
        name,roll,email = st.text_input("Name"),st.text_input("Roll"),st.text_input("Email")
        branch=st.selectbox("Branch",get_branches()); semester=st.selectbox("Sem",get_semesters()); section=st.selectbox("Sec",get_sections())
        if st.button("Add Student"): 
            Student.objects.create(name=name,roll_number=roll,email=email,branch=branch,semester=semester,section=section)
            st.success("Added")
    qs=apply_academic_filters(Student.objects.all(),"stu")
    df=pd.DataFrame([{'Name':s.name,'Roll':s.roll_number,'Email':s.email,'Br':s.branch,'Sem':s.semester,'Sec':s.section} for s in qs])
    st.download_button("Export CSV",df.to_csv(index=False),"stu.csv"); st.table(df)

def teacher_list():
    if st.session_state.role!="ADMIN": st.error("Admins only"); return
    page_header("Manage Teachers","Add/search/filter/export")
    with st.expander("➕ Add New Teacher"):
        u,e,p=st.text_input("Username"),st.text_input("Email"),st.text_input("Password",type="password")
        b=st.selectbox("Branch",get_branches()); sm=st.selectbox("Sem",get_semesters()); sc=st.selectbox("Sec",get_sections())
        if st.button("Add Teacher"):
            CustomUser.objects.create_user(username=u,email=e,password=p,role=CustomUser.Roles.TEACHER,branch=b,semester=sm,section=sc)
            st.success("Added")
    qs=apply_academic_filters(CustomUser.objects.filter(role=CustomUser.Roles.TEACHER),"tea")
    df=pd.DataFrame([{'User':t.username,'Email':t.email,'Br':t.branch,'Sem':t.semester,'Sec':t.section} for t in qs])
    st.download_button("Export CSV",df.to_csv(index=False),"tea.csv"); st.table(df)

# --- Admin: View All Attendance Records ---
def all_attendance_records():
    if st.session_state.get("role") != "ADMIN":
        st.error("Access denied: Admins only.")
        return

    page_header("All Attendance Records", "Filter by date, export full logs.")
    # Date filter
    start = st.date_input("Start date", datetime.date.today() - datetime.timedelta(days=30), key="att_start")
    end = st.date_input("End date", datetime.date.today(), key="att_end")
    records = AttendanceRecord.objects.select_related('student', 'marked_by').filter(date__range=(start, end)).order_by('-date')

    # Export
    df = pd.DataFrame([{
        'Date': r.date, 'Student': r.student.name, 'Roll': r.student.roll_number,
        'Status': r.status, 'Marked By': r.marked_by.username if r.marked_by else ''
    } for r in records])
    csv = df.to_csv(index=False)
    st.download_button("⬇️ Export Records CSV", csv, "attendance.csv", "text/csv")

    st.dataframe(df)

# --- Admin: Monthly Reports ---
def monthly_reports():
    if st.session_state.get("role") != "ADMIN":
        st.error("Access denied: Admins only.")
        return

    page_header("Monthly Attendance Report", "Select student and download report.")
    report = generate_monthly_report()
    student = st.selectbox("Select student", list(report.keys()), key="report_student")
    data = report.get(student, {})

    if not data:
        st.info("No records available.")
        return

    # Prepare table & export
    rows = []
    for m, vals in data.items():
        rows.append({ 'Month': m, 'Present': vals['present'], 'Absent': vals['absent'], 'Percentage': vals['percentage'] })
    df = pd.DataFrame(rows)
    st.download_button("⬇️ Download Report CSV", df.to_csv(index=False), f"report_{student}.csv", "text/csv")

    st.table(df)

    # Chart
    fig, ax = plt.subplots()
    ax.plot(df['Month'], df['Percentage'], marker='o')
    ax.set_ylabel('Attendance %')
    ax.set_title(f'Attendance % for {student}')
    ax.grid(True)
    st.pyplot(fig)

# --- Admin: Send Low Attendance Alerts ---
def send_alerts_admin():
    if st.session_state.get("role") != "ADMIN":
        st.error("Access denied: Admins only.")
        return

    page_header("Send Low Attendance Alerts", "Send email warnings to students below threshold.")
    threshold = st.slider("Threshold %", min_value=50, max_value=100, value=75, step=5, key="alert_threshold")
    if st.button("Send Alerts", key="send_alerts_admin_btn"):
        emails = send_low_attendance_alerts(threshold)
        if emails:
            st.success(f"Alerts sent to: {', '.join(emails)}")
        else:
            st.info("No students below threshold.")
