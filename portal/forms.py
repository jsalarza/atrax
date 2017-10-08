from django import forms
from django.contrib.auth.models import User
from .models import LiteratureType, Literature


class LiteratureTypeForm(forms.ModelForm):

    class Meta:
        model = LiteratureType
        fields = ['lit_type_name']


class LiteratureForm(forms.ModelForm):

    class Meta:
        model = Literature
        fields = ['lit_title', 'lit_desc', 'lit_genre', 'lit_author', 'lit_file']

        labels = {
            'lit_title': 'Title',
            'lit_desc': 'Description',
            'lit_genre': 'Genre',
            'lit_author': 'Author',
            'lit_file': 'File',
        }

class LiteratureForm_b(forms.ModelForm):

    class Meta:
        model = Literature
        fields = ['lit_type', 'lit_title', 'lit_desc', 'lit_genre', 'lit_author', 'lit_file']

        labels = {
            'lit_type': 'Type',
            'lit_title': 'Title',
            'lit_desc': 'Description',
            'lit_genre': 'Genre',
            'lit_author': 'Author',
            'lit_file': 'File',
        }


class UserForm(forms.ModelForm):

    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    username = forms.CharField(widget=forms.EmailInput, required=True, label='Email')

    class Meta:
        model = User
        fields = ['first_name', 'last_name',  'username', 'password', 'confirm_password']
