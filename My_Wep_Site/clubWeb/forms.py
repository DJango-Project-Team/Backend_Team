from django import forms
from .models import Application

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application  # Application 모델을 기반으로 폼을 생성
        fields = ['student_name', 'student_id', 'email', 'motivation', 'experience']  # 제출할 필드들
