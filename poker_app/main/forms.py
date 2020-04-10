from django import forms

from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']
        labels = {'username': 'Username:'}

class LoginForm(forms.Form):
    username = forms.CharField(label='Username:')
