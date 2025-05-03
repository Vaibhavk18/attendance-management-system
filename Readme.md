# Attendance Management System

A production‑grade attendance tracking platform built with Django (PostgreSQL via Supabase) and Streamlit.

## Features

- Role‑based authentication (Admin & Teacher)  
- Branch / Semester / Section segregation  
- Automated attendance marking (past 6 months mock data)  
- Monthly reports with charts  
- Email alerts for low attendance  
- CSV export of students, teachers, and attendance logs  

## Tech Stack

- **Backend**: Django, Supabase (PostgreSQL), Django ORM  
- **Frontend**: Streamlit, Matplotlib, Pandas  
- **Email**: Gmail SMTP (App Password)  
- **Deployment**: Streamlit Community Cloud  

## Setup (Local)

1. **Clone repo**  
   ```bash
   git clone https://github.com/<your‑username>/attendance-management-system.git
   cd attendance-management-system
2. **Activate Virtual Environment**
    python -m venv venv
    # Windows:
    .\\venv\\Scripts\\activate
    # macOS/Linux:
    source venv/bin/activate

3. **Install Requirements** 
    pip install -r backend/requirements.txt
    pip install streamlit
4. **Configure .env**
    Copy .env.example to .env and fill in your Supabase & SMTP credentials.
5. **Run Migrations**
   python backend/manage.py makemigrations
   python backend/manage.py migrate

6. **Create Superuser**
   python backend/manage.py createsuperuser
7. **Populate mock data (optional)**
   python backend/manage.py shell
   # paste the mock‑data script…
8. **Streamlit UI**
   streamlit run frontend/main.py





