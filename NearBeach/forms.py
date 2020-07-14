from __future__ import unicode_literals
from django import forms

#Import from Models
from .models import *

class SearchForm(forms.Form):
    #Just have a simple search field
    search=forms.CharField()