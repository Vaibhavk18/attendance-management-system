from django.contrib import admin
from .models import CustomUser, Student, AttendanceRecord
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username','email','role','branch','semester','section','is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Academic Info', {'fields':('role','branch','semester','section')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Student)
admin.site.register(AttendanceRecord)
