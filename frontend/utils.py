import os
import sys
import django
from django.apps import apps

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
BACKEND_DIR = os.path.join(BASE_DIR, 'backend')
sys.path.insert(0, BACKEND_DIR)


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'attendance_system.settings')

def setup_django():
    """Configure Django settings so Streamlit can use the ORM."""
    # Only setup if not already done
    if not apps.ready:
        django.setup()
