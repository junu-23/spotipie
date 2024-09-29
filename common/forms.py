# 회원가입 시 사용할 UserForm

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(label='이메일')

    class Meta:
        model = User
        # 장고에서 User모델은 이미 기본적으로 제공되는 인증 모델
        fields = ('username', 'password1', 'password2', 'email')
