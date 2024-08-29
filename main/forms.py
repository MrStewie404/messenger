# from django import forms
# from .models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    # username = forms.CharField(widget=forms.Textarea(attrs={'class': 'username_input'}))
    # avatar = serializers.CharField(source="avatar.url")
    
    class Meta:
        model = User
        fields = [
            'username',
            # 'avatar',
            'password1',
            'password2',
        ]

class LoginForm(AuthenticationForm):
    # username = forms.CharField(widget=forms.Textarea(attrs={'class': 'username_input'}))
    # avatar = serializers.CharField(source="avatar.url")
    
    class Meta:
        model = User
        fields = [
            'username',
            # 'avatar',
            'password',
            # 'password2',
        ]