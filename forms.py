from django import forms

#Import from Models
from .models import organisations

#Import extra
import datetime

class new_project_form(forms.Form):
	#SQL needed for form
	organisations_results = organisations.objects.all()
	
	project_name = forms.CharField(max_length = 255)
	project_description = forms.CharField(widget = forms.Textarea)
	organisations_id = forms.ModelChoiceField(label = "Organisation", widget = forms.Select, queryset = organisations_results)

