from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from base_app.models import CustomUser


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class CustomUserForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'
        exclude = ['user']
