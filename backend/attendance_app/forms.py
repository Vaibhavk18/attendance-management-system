from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser, Student, AttendanceRecord

class CustomUserSignupForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username','email','role',
            'branch','semester','section',
            'password1','password2'
        )

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name','roll_number','email','branch','semester','section']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = AttendanceRecord
        fields = ['student','date','status']

class TeacherCreationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = CustomUser
        fields = (
            'username','email','password','role',
            'branch','semester','section'
        )

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
