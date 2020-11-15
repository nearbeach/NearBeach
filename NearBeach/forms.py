from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm

# Import from Models
from .models import *


class AddBugForm(forms.Form):
    bug_client = forms.ModelChoiceField(
        required=True,
        queryset=bug_client.objects.filter(
            is_deleted=False,
        )
    )
    bug_id = forms.IntegerField(
        required=True,
        min_value=0,
    )
    bug_description = forms.CharField(
        required=True,
    )
    bug_status = forms.CharField(
        required=True,
    )


class AddCustomerForm(forms.Form):
    customer = forms.ModelChoiceField(
        required=True,
        queryset=customer.objects.all(),
    )


class AddFolderForm(forms.Form):
    folder_description = forms.CharField(
        required=True,
        max_length=50,
    )
    parent_folder = forms.ModelChoiceField(
        required=False,
        queryset=folder.objects.all(),
    )


class AddGroupForm(forms.Form):
    group_list = forms.ModelMultipleChoiceField(
        required=True,
        queryset=group.objects.all(),
    )


class AddKanbanLinkForm(forms.Form):
    project = forms.ModelChoiceField(
        required=False,
        queryset=project.objects.filter(
            is_deleted=False,
        )
    )
    requirement = forms.ModelChoiceField(
        required=False,
        queryset=requirement.objects.filter(
            is_deleted=False,
        )
    )
    task = forms.ModelChoiceField(
        required=False,
        queryset=task.objects.filter(
            is_deleted=False,
        )
    )
    kanban_column = forms.ModelChoiceField(
        required=True,
        queryset=kanban_column.objects.filter(
            is_deleted=False,
        )
    )
    kanban_level = forms.ModelChoiceField(
        required=True,
        queryset=kanban_level.objects.filter(
            is_deleted=False,
        )
    )


class AddLinkForm(forms.Form):
    document_description = forms.CharField(
        max_length=50,
        required=True,
    )
    document_url_location = forms.URLField(
        required=True,
    )
    parent_folder = forms.ModelChoiceField(
        required=False,
        queryset=folder.objects.all(),
    )


class AddNoteForm(forms.Form):
    note = forms.CharField(
        required=True,
    )


class AddRequirementLinkForm(forms.Form):
    # One external field
    project = forms.ModelMultipleChoiceField(
        required=False,
        queryset=project.objects.filter(
            is_deleted=False,
        )
    )
    task = forms.ModelMultipleChoiceField(
        required=False,
        queryset=task.objects.filter(
            is_deleted=False,
        )
    )


class CheckKanbanBoardName(forms.Form):
    kanban_board_name = forms.CharField(max_length=255)


class CustomerForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = customer
        fields = [
            'customer_title',
            'customer_first_name',
            'customer_last_name',
            'customer_email',
            'organisation',
        ]


class DocumentUploadForm(ModelForm):
    document = forms.FileField(
        required=True,
    )
    parent_folder = forms.ModelChoiceField(
        required=False,
        queryset=folder.objects.all(),
    )

    class Meta:
        model = document
        fields = {
            'document',
            'document_description',
        }


class AddUserForm(forms.Form):
    user_list = forms.ModelMultipleChoiceField(
        required=True,
        queryset=User.objects.all(),
    )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'class': 'form-control',
            'required': True,
            'autofocus': True,
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'class': 'form-control',
            'required': True,
        })
    )


class MoveKanbanCardForm(forms.Form):
    # Get Query Sets
    kanban_column_results = kanban_column.objects.all()
    kanban_level_results = kanban_level.objects.all()

    # New card information
    new_card_column = forms.ModelChoiceField(
        required=True,
        queryset=kanban_column_results,
    )
    new_card_level = forms.ModelChoiceField(
        required=True,
        queryset=kanban_level_results,
    )
    new_card_sort_number = forms.IntegerField()

    # Old card information
    old_card_column = forms.ModelChoiceField(
        required=True,
        queryset=kanban_column_results,
    )
    old_card_level = forms.ModelChoiceField(
        required=True,
        queryset=kanban_level_results,
    )
    old_card_sort_number = forms.IntegerField()




class NewCustomerForm(forms.ModelForm):
    organisation = forms.ModelChoiceField(
        queryset=organisation.objects.all(),
        required=False,
    )

    # Basic Meta Data
    class Meta:
        model = customer
        fields = [
            'customer_title',
            'customer_first_name',
            'customer_last_name',
            'customer_email',
            'organisation',
        ]


class NewKanbanCardForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = kanban_card
        fields = [
            'kanban_card_text',
            'kanban_level',
            'kanban_column',
        ]


class NewKanbanForm(forms.ModelForm):
    column_title = forms.SelectMultiple()
    level_title = forms.SelectMultiple()

    # Basic Meta Data
    class Meta:
        model = kanban_board
        fields = [
            'kanban_board_name',
        ]


class NewProjectForm(forms.ModelForm):
    project_start_date = forms.DateTimeField(
        input_formats=['c'],
    )
    project_end_date = forms.DateTimeField(
        input_formats=['c'],
    )
    group_list = forms.ModelMultipleChoiceField(
        required=True,
        queryset=group.objects.filter(
            is_deleted=False,
        )
    )

    # Basic Meta Data
    class Meta:
        model = project
        fields = [
            'project_name',
            'project_description',
            'project_start_date',
            'project_end_date',
            'organisation',
        ]


class NewTaskForm(forms.ModelForm):
    task_start_date = forms.DateTimeField(
        input_formats=['c'],
    )
    task_end_date = forms.DateTimeField(
        input_formats=['c'],
    )
    group_list = forms.ModelMultipleChoiceField(
        required=True,
        queryset=group.objects.filter(
            is_deleted=False,
        )
    )

    # Basic Meta Data
    class Meta:
        model = task
        fields = [
            'task_short_description',
            'task_long_description',
            'task_start_date',
            'task_end_date',
            'organisation',
        ]


class OrganisationForm(forms.ModelForm):
    # Basic Meta data
    class Meta:
        model = organisation
        fields = [
            'organisation_name',
            'organisation_website',
            'organisation_email',
        ]


class OrganisationProfilePictureForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        fields = [
            'organisation_picture'
        ]


class ProjectForm(forms.ModelForm):
    project_start_date = forms.DateTimeField(
        input_formats=['c'],
    )
    project_end_date = forms.DateTimeField(
        input_formats=['c'],
    )

    # Basic Meta Data
    class Meta:
        model = project
        fields = [
            'project_name',
            'project_description',
            'project_start_date',
            'project_end_date',
        ]


class NewRequirementItemForm(forms.ModelForm):
    # Basic Meta data
    class Meta:
        model = requirement_item
        fields = [
            'requirement_item_title',
            'requirement_item_scope',
            'requirement_item_status',
            'requirement_item_type',
        ]


class NewRequirementForm(forms.ModelForm):
    # One external field
    group_list = forms.ModelMultipleChoiceField(
        required=True,
        queryset=group.objects.filter(
            is_deleted=False,
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


class QueryBugClientForm(forms.Form):
    bug_client_id = forms.ModelChoiceField(
        required=True,
        queryset=bug_client.objects.filter(
            is_deleted=False,
        )
    )
    search = forms.CharField(
        max_length=50,
    )


class SearchForm(forms.Form):
    # Just have a simple search field
    search = forms.CharField(
        required=False,
    )


class SearchObjectsForm(forms.Form):
    include_closed = forms.BooleanField(
        required=False,
        initial=False,
    )
    search = forms.CharField(
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


class UpdateRequirementItemForm(forms.ModelForm):
    # Basic Meta data
    class Meta:
        model = requirement_item
        fields = [
            'requirement_item_title',
            'requirement_item_scope',
            'requirement_item_status',
            'requirement_item_type',
        ]
