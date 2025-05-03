from utils import setup_django
setup_django()

import streamlit as st
from django.contrib.auth import authenticate
from attendance_app.models import CustomUser,BRANCH_CHOICES,SEMESTER_CHOICES,SECTION_CHOICES

def login():
    st.subheader("🔑 Login")
    username = st.text_input("Username", key="login_username")
    password = st.text_input("Password", type="password", key="login_password")
    if st.button("Login", key="login_btn"):
        user = authenticate(username=username.strip(), password=password)
        if user:
            st.session_state.user = username
            st.session_state.role = 'ADMIN' if user.is_superuser else user.role
            st.session_state.authenticated = True
            st.success(f"Logged in as {username}")
            st.rerun()
        else:
            st.error("Invalid credentials")

def signup():
    st.subheader("📝 Signup")
    username = st.text_input("Choose a username", key="su_username")
    email = st.text_input("Email", key="su_email")
    password = st.text_input("Password", type="password", key="su_password")
    role = st.selectbox("Role", ["Teacher"], key="su_role")
    branch = st.selectbox("Branch", [b for b,_ in BRANCH_CHOICES], key="su_branch")
    semester = st.selectbox("Semester", [s for s,_ in SEMESTER_CHOICES], key="su_semester")
    section = st.selectbox("Section", [sec for sec,_ in SECTION_CHOICES], key="su_section")
    if st.button("Create account", key="signup_btn"):
        if CustomUser.objects.filter(username=username).exists():
            st.error("Username taken")
        else:
            CustomUser.objects.create_user(
                username=username,
                email=email,
                password=password,
                role=role.upper(),
                branch=branch,
                semester=semester,
                section=section
            )
            st.success("Account created—please log in.")
