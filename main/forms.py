from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from main.models import Avatars, Updates

class SignUpForm(UserCreationForm):
    # username = forms.CharField(widget=forms.Textarea(attrs={'class': 'username_input'}))
    # avatar = serializers.CharField(source="avatar.url")
    
    class Meta:
        model = User
        fields = [
            'username',
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
            'password',
        ]

class AvatarForm(forms.ModelForm):
    class Meta:
        model = Avatars
        fields = ['path']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'username']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Updates
        fields = ['title', 'text']