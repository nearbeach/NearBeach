from __future__ import unicode_literals
from django import forms
from django.forms import ModelForm

# Import from Models
from .models import folder, group, tag, User, change_task, customer, kanban_column, kanban_level, tag_assignment, kanban_card, kanban_board, permission_set, project, request_for_change, requirement_item, requirement, task, organisation, bug_client, document


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


class AddObjectLinkForm(forms.Form):
    project = forms.ModelMultipleChoiceField(
        queryset=project.objects.all(),
        required=False,
    )
    requirement = forms.ModelMultipleChoiceField(
        queryset=requirement.objects.all(),
        required=False,
    )
    requirement_item = forms.ModelMultipleChoiceField(
        queryset=requirement_item.objects.all(),
        required=False,
    )
    task = forms.ModelMultipleChoiceField(
        queryset=task.objects.all(),
        required=False,
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


class AddTagsForm(forms.Form):
    tag_id = forms.ModelMultipleChoiceField(
        queryset=tag.objects.all(),
    )


class AdminAddUserForm(forms.Form):
    group = forms.ModelMultipleChoiceField(
        queryset=group.objects.all(),
    )
    permission_set = forms.ModelMultipleChoiceField(
        queryset=permission_set.objects.all(),
    )
    username = forms.ModelChoiceField(
        queryset=User.objects.all(),
    )


class ChangeTaskForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = change_task
        fields = [
            'change_task_title',
            'change_task_description',
            'change_task_start_date',
            'change_task_end_date',
            'change_task_seconds',
            'change_task_required_by',
            'is_downtime',
        ]


class ChangeTaskStatusForm(forms.ModelForm):
    class Meta:
        model = change_task
        fields = [
            'change_task_status',
        ]


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


class DeleteColumnForm(forms.Form):
    delete_item_id = forms.ModelChoiceField(
        queryset=kanban_column.objects.all(),
        required=True,
    )
    destination_item_id = forms.ModelChoiceField(
        queryset=kanban_column.objects.all(),
        required=True,
    )


class DeleteLevelForm(forms.Form):
    delete_item_id = forms.ModelChoiceField(
        queryset=kanban_level.objects.all(),
        required=True,
    )
    destination_item_id = forms.ModelChoiceField(
        queryset=kanban_level.objects.all(),
        required=True,
    )


class DeleteTagForm(forms.ModelForm):
    class Meta:
        model = tag_assignment
        fields = {
            'tag',
            'object_enum',
            'object_id',
        }


class DocumentUploadForm(forms.ModelForm):
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


class KanbanCardForm(forms.ModelForm):
    kanban_card_id = forms.ModelChoiceField(
        required=True,
        queryset=kanban_card.objects.all(),
    )
    kanban_card_description = forms.CharField(
        required=False,
    )
    kanban_column = forms.ModelChoiceField(
        required=True,
        queryset=kanban_column.objects.all()
    )
    kanban_level = forms.ModelChoiceField(
        required=True,
        queryset=kanban_level.objects.all(),
    )

    class Meta:
        model = kanban_card
        fields = {
            'kanban_card_id',
            'kanban_card_text',
            'kanban_card_description',
            'kanban_column',
            'kanban_level',
        }


class KanbanCardArchiveForm(forms.Form):
    kanban_card_id = forms.ModelMultipleChoiceField(
        required=True,
        queryset=kanban_card.objects.all(),
    )


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


class NewChangeTaskForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = change_task
        fields = [
            'request_for_change',
            'change_task_title',
            'change_task_description',
            'change_task_start_date',
            'change_task_end_date',
            'change_task_seconds',
            # 'change_task_assigned_user',
            # 'change_task_qa_user',
            'change_task_required_by',
            'is_downtime',
        ]


class NewColumnForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = kanban_column
        fields = [
            'kanban_column_name',
            'kanban_column_sort_number',
        ]


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


class NewGroupForm(forms.ModelForm):
    parent_group = forms.ModelChoiceField(
        queryset=group.objects.all(),
        required=False,
    )

    # Basic Meta Data
    class Meta:
        model = group
        fields = [
            'group_name',
            'parent_group',
        ]


class NewKanbanCardForm(forms.ModelForm):
    kanban_card_description = forms.CharField(
        required=False,
    )

    # Basic Meta Data
    class Meta:
        model = kanban_card
        fields = [
            'kanban_card_text',
            'kanban_card_description',
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


class NewLevelForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = kanban_level
        fields = [
            'kanban_level_name',
            'kanban_level_sort_number',
        ]


class NewPermissionSetForm(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = permission_set
        fields = [
            'permission_set_name',
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


class NewRequestForChangeForm(forms.ModelForm):
    group_list = forms.ModelMultipleChoiceField(
        required=True,
        queryset=group.objects.filter(
            is_deleted=False,
        )
    )

    # Basic Meta Data
    class Meta:
        model = request_for_change
        fields = [
            'rfc_title',
            'rfc_summary',
            'rfc_type',
            'rfc_implementation_start_date',
            'rfc_implementation_end_date',
            'rfc_implementation_release_date',
            'rfc_version_number',
            'rfc_lead',
            'rfc_priority',
            'rfc_risk',
            'rfc_impact',
            'rfc_risk_and_impact_analysis',
            'rfc_implementation_plan',
            'rfc_backout_plan',
            'rfc_test_plan',
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


class NewTagForm(forms.ModelForm):
    class Meta:
        model = tag
        fields = [
            'tag_name',
            'tag_colour',
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


class NewUserForm(forms.ModelForm):
    password1 = forms.CharField(
        max_length=255,
        required=True,
    )
    password2 = forms.CharField(
        max_length=255,
        required=True,
    )

    # Basic Meta data
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
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


class PasswordResetForm(forms.Form):
    password = forms.CharField(
        max_length=50,
        required=True,
    )
    username = forms.ModelChoiceField(
        queryset=User.objects.all(),
        required=True,
    )


class PermissionSetForm(forms.ModelForm):
    class Meta:
        model = permission_set
        exclude = [
            'change_user',
            'is_deleted',
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
            'project_status',
        ]


class ResortColumnForm(forms.Form):
    item = forms.ModelMultipleChoiceField(
        queryset=kanban_column.objects.all(),
        required=True,
    )


class ResortLevelForm(forms.Form):
    item = forms.ModelMultipleChoiceField(
        queryset=kanban_level.objects.all(),
        required=True,
    )


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


class RfcModuleForm(forms.Form):
    # This form is for all the sub modules that need to be saved separately.
    text_input = forms.CharField(
        required=True,
    )
    priority_of_change = forms.IntegerField(
        required=False,
    )
    risk_of_change = forms.IntegerField(
        required=False,
    )
    impact_of_change = forms.IntegerField(
        required=False,
    )


class RfcInformationSaveForm(forms.ModelForm):
    class Meta:
        model = request_for_change
        fields = [
            'rfc_title',
            'rfc_summary',
            'rfc_type',
            'rfc_version_number',
            'rfc_implementation_start_date',
            'rfc_implementation_end_date',
            'rfc_implementation_release_date',
        ]


class SearchForm(forms.Form):
    # Just have a simple search field
    search = forms.CharField(
        max_length=250,
        required=False,
    )


class SearchObjectsForm(forms.Form):
    include_closed = forms.BooleanField(
        required=False,
        initial=False,
    )
    search = forms.CharField(
        max_length=250,
        required=False,
    )


class TagForm(forms.Form):
    tag_id = forms.IntegerField(required=True)
    tag_name = forms.CharField(
        required=True,
        max_length=50,
    )
    tag_colour = forms.CharField(
        required=True,
        max_length=7,
    )


class TaskInformationForm(forms.ModelForm):
    # Basic Meta data
    class Meta:
        model = task
        fields = [
            'task_short_description',
            'task_long_description',
            'task_start_date',
            'task_end_date',
            'task_status',
        ]


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


class UpdateRFCStatus(forms.ModelForm):
    # Basic Meta Data
    class Meta:
        model = request_for_change
        fields = [
            'rfc_status',
        ]


class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=255,
        required=True,
    )
    last_name = forms.CharField(
        max_length=255,
        required=True,
    )
    email = forms.EmailField(
        max_length=255,
        required=False,
    )
    # Basic Meta Data
    class Meta:
        model = User
        fields = [
            'email',
            'first_name',
            'last_name',
            'is_active',
            'is_superuser',
        ]
