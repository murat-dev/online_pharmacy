from django import forms
from crispy_forms.helper import FormHelper
from django.contrib.auth.models import User

from main.models import Tag


class RegistrationForm(forms.ModelForm):
    password = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput)
    password_confirmation = forms.CharField(min_length=6, required=True, widget=forms.PasswordInput)
    # tag = forms.ModelChoiceField(queryset=Tag.objects.all(), empty_label=('Nothing'))

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username',
                  'password', 'password_confirmation', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("User with given username already exists")
        return username

    def clean(self):
        data = self.cleaned_data
        password = data.get('password')
        password_confirmation = data.pop('password_confirmation')
        if password != password_confirmation:
            raise forms.ValidationError("Passwords don't match")
        return data

    def save(self, commit=True):
        user = User.objects.create_user(**self.cleaned_data)
        return user