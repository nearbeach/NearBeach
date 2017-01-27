from django import forms
import datetime

class new_project_form(forms.Form):
	project_name = forms.CharField(max_length = 255)
	project_description = forms.CharField(widget = forms.Textarea)
	organisations_id = forms.CharField()
	project_start_date = forms.DateTimeField(widget = forms.DateTimeInput)
	project_end_date = forms.DateTimeField(widget = forms.DateTimeInput)
