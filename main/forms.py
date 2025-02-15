from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from main.models import Avatars, Updates, Modules, AddedModules, UserSupplement
from django.forms.models import inlineformset_factory

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = [
            'username',
            'password1',
            'password2',
        ]

class LoginForm(AuthenticationForm):
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

class DescriptionForm(forms.ModelForm):
    class Meta:
        model = UserSupplement
        fields = ['description']

class ModulesChoiceForm(forms.Form):
    def __init__(self, *args, **kwargs):
        queryset = kwargs.pop('queryset', None)
        super().__init__(*args, **kwargs)
        if queryset is not None:
             self.fields['modules'].queryset = queryset

    modules = forms.ModelMultipleChoiceField(
        queryset=AddedModules.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Выберите модули'
    )

class ModuleDetailsForm(forms.ModelForm):
    class Meta:
        model = AddedModules
        fields = ['height', 'width', 'visibility_for_others', 'visible']

class ModulesFormSearch(forms.ModelForm):
        class Meta:
           model = Modules
           fields = ['name']

class ModulesFormCreate(forms.ModelForm):
        class Meta:
           model = Modules
           fields = ['name', 'description', 'path', 'visible_in_public']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'username']


class UpdateForm(forms.ModelForm):
    class Meta:
        model = Updates
        fields = ['title', 'text']