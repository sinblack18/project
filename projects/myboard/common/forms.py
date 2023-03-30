# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User


# UserCreationForm을 상속 받는 UserForm을 작성
class UserForm(UserCreationForm):  # 파이썬에서 클래스 ()안에 들어가는 것은 상속 받을 것
    email = forms.EmailField(label="이메일")
    first_name = forms.CharField(label="이름")
    last_name = forms.CharField(label="성")

    class Meta:  # 폼의 정보를 담고 있는 내부 클래스
        model = User
        fields = ("username", "email", "first_name", "last_name")


class CustomchangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name")
