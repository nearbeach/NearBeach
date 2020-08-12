from __future__ import unicode_literals
from django import forms

#Import from Models
from .models import *


class login_form(forms.Form):
    username=forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'required': True,
            'autofocus': True,
        })
    )
    password=forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'required': True,
        })
    )

class NewRequirementForm(forms.ModelForm):
    # One external field
    group_list=forms.ModelMultipleChoiceField(
        required=True,
        queryset=group.objects.filter(
            is_deleted="FALSE",
        )
    )

    # Basic Meta data
    class Meta:
        model = requirement
        fields = [
            'requirement_title',
            'requirement_scope',
            'requirement_status',
            'requirement_type',
            'organisation',
        ]


class SearchForm(forms.Form):
    #Just have a simple search field
    search=forms.CharField(
        required=False,
    )


class UpdateRequirementForm(forms.ModelForm):
    # Basic Meta data
    class Meta:
        model = requirement
        fields = [
            'requirement_title',
            'requirement_scope',
            'requirement_status',
            'requirement_type',
        ]