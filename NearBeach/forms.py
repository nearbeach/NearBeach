from __future__ import unicode_literals
from django import forms

#Import from Models
from .models import *

class NewRequirementForm(forms.ModelForm):
    # One external field
    """
    group_list=forms.MultipleChoiceField(
        required=True,
        choices=group.objects.filter(
            is_deleted="FALSE",
        )
    )
    """

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