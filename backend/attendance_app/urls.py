from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('signup/', views.signup, name='signup'),

    path('students/', views.student_list, name='student_list'),
    path('students/add/', views.add_student, name='add_student'),

    path('attendance/', views.mark_attendance, name='mark_attendance'),
    path('reports/', views.attendance_report, name='attendance_report'),
    path('report/', views.monthly_attendance_report, name='monthly_report'),
    path('api/graph-data/', views.graph_data_api, name='graph_data'),
    path('admin/students/<int:student_id>/edit/', views.edit_student, name='edit_student'),
    path('admin/students/<int:student_id>/delete/', views.delete_student, name='delete_student'),
    path('admin/teachers/', views.teacher_list, name='teacher_list'),
    path('admin/teachers/add/', views.create_teacher, name='create_teacher'),
    path('admin/attendance/', views.all_attendance_records, name='all_attendance'),
    path('admin/reports/monthly/', views.view_monthly_report, name='monthly_report'),




]
