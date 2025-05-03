
import streamlit as st
from auth import login, signup
from dashboard import show_dashboard

st.set_page_config(page_title="Attendance System", layout="wide")

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

st.title("🎓 Attendance Management System")

if not st.session_state.authenticated:
    choice = st.sidebar.radio("Go to", ["Login", "Signup"])
    if choice == "Login":
        login()
    else:
        signup()
else:
    show_dashboard()
