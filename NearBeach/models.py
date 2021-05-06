from __future__ import unicode_literals
from django.db import models, connection
from .private_media import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

# ENUM choices
DISCOUNT_CHOICE = (
    ('Percentage', 'Percentage'),
    ('Amount', 'Amount'),
)

KANBAN_BOARD_STATUS_CHOICE = (
    ('Open', 'Open'),
    ('Closed', 'Closed'),
)

PAGE_LAYOUT = (
    ('Landscape', 'Landscape'),
    ('Portrait', 'Portrait'),
)

PERMISSION_LEVEL = (
    (0, 'No Permission'),
    (1, 'Read Only'),
    (2, 'Edit Only'),
    (3, 'Add and Edit'),
    (4, 'Full Permission'),
)

PERMISSION_BOOLEAN = (
    (0, 'No Permission'),
    (1, 'Has Permission'),
)

PROJECT_STATUS_CHOICE = (
    ('New', 'New'),
    ('Backlog', 'Backlog'),
    ('Blocked', 'Blocked'),
    ('In Progress', 'In Progress'),
    ('Test/Review', 'Test/Review'),
    ('Closed', 'Closed'),
)

QUOTE_APPROVAL_STATUS = (
    ('REJECTED', 'REJECTED'),
    ('DRAFT', 'DRAFT'),
    ('APPROVED', 'APPROVED'),
)

RATING_SCORE = (
    (1, '1 Star'),
    (2, '2 Star'),
    (3, '3 Star'),
    (4, '4 Star'),
    (5, '5 Star'),
)

RFC_APPROVAL = (
    (1, 'Waiting'),
    (2, 'Approved'),
    (3, 'Rejected'),
    (4, 'Cancel'),
)

RFC_IMPACT = (
    (3, 'High'),
    (2, 'Medium'),
    (1, 'Low'),
)

RFC_PRIORITY = (
    (4, 'Critical'),
    (3, 'High'),
    (2, 'Medium'),
    (1, 'Low'),
)

RFC_RISK = (
    (5, 'Very High'),
    (4, 'High'),
    (3, 'Moderate'),
    (2, 'Low'),
    (1, 'None'),
)

RFC_STATUS = (
    (1, 'Draft'),
    (2, 'Waiting for approval'),
    (3, 'Approved'),
    (4, 'Started'),
    (5, 'Finished'),
    (6, 'Rejected'),
)

RFC_TYPE = (
    (4, 'Emergency'),
    (3, 'High'),
    (2, 'Medium'),
    (1, 'Low'),
)

WANT_CHOICE = (
    ('0', 'Do not want to do'),
    ('1', 'Want to do'),
)
SKILL_CHOICE = (
    ('0', 'Can not do'),
    ('1', 'Willing to learn'),
    ('2', 'Knows a little'),
    ('3', 'Knows a lot'),
    ('4', 'Proficient'),
)

WEBSITE_SOURCE = (
    ('Twitter', 'Twitter'),
    ('Facebook', 'Facebook'),
    ('Github', 'Github'),
    ('Gitlab', 'Gitlab'),
    ('Website', 'Website'),
    ('LinkedIn', 'LinkedIn'),
    ('Staff Page', 'Staff page'),
    ('Other', 'Other'),
)


# List of tables - in alphabetical order
class about_user(models.Model):
    about_user_id = models.AutoField(primary_key=True)
    about_user_text = models.TextField()
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "about_user"


"""
Contact History is a simple form that user will fill out every time they
have some form of contact with the customer. This table will store both
contact history for customer and Organisations. The customer field in
this instance is not required, and implies that the contact history is 
applied to the organisation. The organisation field will fill out automatically
when a user applies it to a customer. :)
"""


class contact_history(models.Model):
    contact_history_id = models.AutoField(primary_key=True)
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    contact_type = models.ForeignKey(
        'list_of_contact_type',
        on_delete=models.CASCADE,
    )
    contact_date = models.DateTimeField()
    contact_history = models.TextField('contact_history')
    document_key = models.ForeignKey(
        'document',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "contact_history"


class bug(models.Model):
    bug_id = models.AutoField(primary_key=True)
    bug_client = models.ForeignKey(
        'bug_client',
        on_delete=models.CASCADE,
    )
    bug_code = models.CharField(max_length=255)  # Just stores the code of the bug
    bug_description = models.TextField()
    bug_status = models.CharField(max_length=50)  # Updated manually?
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        'requirement',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey \
        (User,
         on_delete=models.CASCADE,
         related_name='%(class)s_change_user',
         )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_description)

    class Meta:
        db_table = "bug"


class bug_client(models.Model):
    bug_client_id = models.AutoField(primary_key=True)
    bug_client_name = models.CharField(max_length=50)
    list_of_bug_client = models.ForeignKey(
        'list_of_bug_client',
        on_delete=models.CASCADE,
    )
    bug_client_url = models.URLField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey \
        (User,
         on_delete=models.CASCADE,
         related_name='%(class)s_change_user',
         )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_client_name)

    class Meta:
        db_table = "bug_client"


class campus(models.Model):
    campus_id = models.AutoField(primary_key=True)
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    campus_nickname = models.CharField(max_length=100)
    campus_phone = models.CharField(
        max_length=20,
        null=True
    )
    campus_fax = models.CharField(
        max_length=20,
        null=True
    )
    campus_address1 = models.CharField(
        max_length=255,
        null=True
    )
    campus_address2 = models.CharField(
        max_length=255,
        null=True
    )
    campus_address3 = models.CharField(
        max_length=255,
        null=True
    )
    campus_suburb = models.CharField(max_length=50)
    campus_region = models.ForeignKey(
        'list_of_country_region',
        on_delete=models.CASCADE,
    )
    campus_postcode = models.CharField(
        max_length=10,
        null=True,
        blank=True,
    )
    campus_country = models.ForeignKey(
        'list_of_country',
        on_delete=models.CASCADE,
    )
    campus_longitude = models.DecimalField(
        decimal_places=13,
        max_digits=16,
        null=True,  # If use has no mapping software, we want to leave this blank
        blank=True,
    )
    campus_latitude = models.DecimalField(
        decimal_places=13,
        max_digits=16,
        null=True,  # If use has no mapping software, we want to leave this blank
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.campus_nickname)

    class Meta:
        db_table = "campus"


class change_task(models.Model):
    change_task_id = models.AutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        'request_for_change',
        on_delete=models.CASCADE,
    )
    change_task_title = models.CharField(
        max_length=255,
    )
    change_task_description = models.TextField(
        blank=True,
        null=True,
    )
    change_task_start_date = models.DateTimeField()
    change_task_end_date = models.DateTimeField()
    change_task_seconds = models.BigIntegerField(
        default=0,
    )
    change_task_assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='change_assigned_user',
    )
    change_task_qa_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='change_qa_user',
    )
    change_task_required_by = models.CharField(
        max_length=255,
        default='Stakeholder(s)',
    )
    change_task_status = models.IntegerField(
        choices=RFC_STATUS,  # Similar FLOW to RFC
    )
    is_downtime = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str('$' + str(self.change_task_title))

    class Meta:
        db_table = "change_task"


class change_task_block(models.Model):
    change_task_blocks = models.ForeignKey(
        change_task,
        on_delete=models.CASCADE,
        related_name='change_task_blocks',
    )
    blocked_change_task = models.ForeignKey(
        change_task,
        on_delete=models.CASCADE,
        related_name='blocked_change_task',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str('$' + str(self.change_task_title))

    class Meta:
        db_table = "change_task_block"


class cost(models.Model):
    cost_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    cost_description = models.CharField(max_length=255, )
    cost_amount = models.DecimalField(
        max_digits=19,
        decimal_places=2
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str('$' + str(self.cost_amount))

    class Meta:
        db_table = "cost"


class customer(models.Model):
    customer_id = models.AutoField(primary_key=True)
    customer_title = models.ForeignKey(
        'list_of_title',
        on_delete=models.CASCADE,
    )
    customer_first_name = models.CharField(max_length=50)
    customer_last_name = models.CharField(max_length=50)
    customer_email = models.CharField(max_length=200)
    customer_profile_picture = models.ImageField(
        blank=True,
        null=True,
        upload_to='profile_pictures'
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(
            str(self.customer_id)
            + ' - '
            + self.customer_first_name
            + ' '
            + self.customer_last_name
        )

    class Meta:
        db_table = "customer"


class customer_campus(models.Model):
    customer_campus_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
    )
    campus = models.ForeignKey(
        'campus',
        on_delete=models.CASCADE,
    )
    customer_phone = models.CharField(max_length=20)
    customer_fax = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "customer_campus"


class document(models.Model):
    document_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    document_description = models.CharField(max_length=255)
    document_url_location = models.TextField(
        # Contains URLS
        null=True,
        blank=True,
    )
    document = models.FileField(
        blank=True,
        null=True,
        storage=File_Storage(),
    )
    whiteboard = models.ForeignKey(
        'whiteboard',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "document"

    def __str__(self):
        return str(self.document_description)


class document_permission(models.Model):
    document_permisssion_id = models.AutoField(primary_key=True)
    document_key = models.ForeignKey(
        'document',
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        'project',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    task = models.ForeignKey(
        'task',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    organisation = models.ForeignKey(
        'organisation',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        'customer',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    opportunity = models.ForeignKey(
        'opportunity',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    whiteboard = models.ForeignKey(
        'whiteboard',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement = models.ForeignKey(
        'requirement',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    requirement_item = models.ForeignKey(
        'requirement_item',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    request_for_change = models.ForeignKey(
        'request_for_change',
        blank=True,
        null=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    folder = models.ForeignKey(
        'folder',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "document_permission"


class email_contact(models.Model):
    email_contact_id = models.AutoField(primary_key=True)
    email_content = models.ForeignKey(
        'email_content',
        on_delete=models.CASCADE,
    )
    to_customer = models.ForeignKey(
        'customer',
        related_name='%(class)s_to_customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    cc_customer = models.ForeignKey(
        'customer',
        related_name='%(class)s_cc_customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    bcc_customer = models.ForeignKey(
        'customer',
        related_name='%(class)s_bcc_customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    opportunity = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    quotes = models.ForeignKey(
        'quote',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    is_private = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "email_contact"


class email_content(models.Model):
    email_content_id = models.AutoField(primary_key=True)
    email_subject = models.CharField(max_length=255)
    email_content = models.TextField('email_content')
    is_private = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "email_content"


class folder(models.Model):
    folder_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        'requirement',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        'requirement_item',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        'request_for_change',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    folder_description = models.CharField(max_length=255)
    parent_folder = models.ForeignKey(
        'self',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.folder_description)

    class Meta:
        db_table = "folder"


class group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(
        max_length=50,
    )
    parent_group = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def natural_key(self):
        return (
            self.group_id,
            self.group_name
        )

    def __str__(self):
        return str(self.group_name)

    class Meta:
        db_table = "group"


class group_manager(models.Manager):
    def get_by_natural_key(
            self,
            group_id,
            group_name
    ):
        return self.get(
            group_id=group_id,
            group_name=group_name
        )


class group_permission(models.Model):
    group_permission_id = models.AutoField(primary_key=True)
    permission_set = models.ForeignKey(
        'permission_set',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        'group',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.permission_set)

    class Meta:
        db_table = "group_permission"


class kanban_board(models.Model):
    kanban_board_id = models.AutoField(primary_key=True)
    kanban_board_name = models.CharField(max_length=255)
    requirement = models.ForeignKey(
        'requirement',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    kanban_board_status = models.CharField(
        max_length=10,
        choices=KANBAN_BOARD_STATUS_CHOICE,
        default="Open",
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_board"

    def __str__(self):
        return str(self.kanban_board_name)


class kanban_card(models.Model):
    kanban_card_id = models.AutoField(primary_key=True)
    kanban_card_text = models.CharField(max_length=255)
    kanban_card_description = models.TextField(
        blank=True,
        null=True,
    )
    kanban_card_sort_number = models.IntegerField()
    kanban_level = models.ForeignKey(
        'kanban_level',
        on_delete=models.CASCADE,
    )
    kanban_column = models.ForeignKey(
        'kanban_column',
        on_delete=models.CASCADE,
    )
    kanban_board = models.ForeignKey(
        'kanban_board',
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        'requirement',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_card"

    def __str__(self):
        return str(self.kanban_card_text)


class kanban_column(models.Model):
    kanban_column_id = models.AutoField(primary_key=True)
    kanban_column_name = models.CharField(max_length=255)
    kanban_column_sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        'kanban_board',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_column"

    def __str__(self):
        return str(self.kanban_column_name)


# class kanban_comment(models.Model):
#     kanban_comment_id = models.AutoField(primary_key=True)
#     kanban_comment = models.TextField()
#     kanban_board = models.ForeignKey(
#         'kanban_board',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#     )
#     kanban_card = models.ForeignKey(
#         'kanban_card',
#         on_delete=models.CASCADE,
#         null=True,
#         blank=True,
#     )
#     user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         null=True
#     )
#     user_infomation = models.CharField(max_length=255)
#     date_created = models.DateTimeField(auto_now_add=True)
#     date_modified = models.DateTimeField(auto_now=True)
#     change_user = models.ForeignKey(
#         User,
#         on_delete=models.CASCADE,
#         related_name='%(class)s_change_user'
#     )
#     is_deleted = models.BooleanField(
#         default=False,
#     )
#
#     class Meta:
#         db_table = "kanban_comment"
#
#     def __str__(self):
#         return str(self.kanban_comment)


class kanban_level(models.Model):
    kanban_level_id = models.AutoField(primary_key=True)
    kanban_level_name = models.CharField(max_length=255)
    kanban_level_sort_number = models.IntegerField()
    kanban_board = models.ForeignKey(
        'kanban_board',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kanban_level"

    def __str__(self):
        return str(self.kanban_level_name)


class kudos(models.Model):
    kudos_key = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=True,
    )
    kudos_rating = models.IntegerField(
        choices=RATING_SCORE,
        default=0,
    )
    improvement_note = models.TextField(
        blank=True,
        null=True,
    )
    liked_note = models.TextField(
        blank=True,
        null=True,
    )
    extra_kudos = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    submitted_kudos = models.BooleanField(
        default=False,
    )
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,

    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "kudos"


class list_of_amount_type(models.Model):
    amount_type_id = models.AutoField(primary_key=True)
    amount_type_description = models.CharField(max_length=20)
    list_order = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.amount_type_description)

    class Meta:
        db_table = "list_of_amount_type"
        ordering = ['list_order']


class list_of_bug_client(models.Model):
    list_of_bug_client_id = models.AutoField(primary_key=True)
    bug_client_name = models.CharField(max_length=50)
    bug_client_api_url = models.CharField(max_length=255)

    # The different API commands
    api_open_bugs = models.CharField(max_length=255)  # Find all open bugs
    api_search_bugs = models.CharField(max_length=255)  # Search command
    api_bug = models.CharField(max_length=255)  # Get that particular bug information - direct link to bug

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.bug_client_name)

    class Meta:
        db_table = "list_of_bug_client"


class list_of_currency(models.Model):
    currency_id = models.AutoField(primary_key=True)
    currency_description = models.CharField(max_length=20)
    currency_short_description = models.CharField(max_length=4)
    list_order = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.currency_description)

    class Meta:
        db_table = "list_of_currency"


class list_of_contact_type(models.Model):
    contact_type_id = models.AutoField(primary_key=True)
    contact_type = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.contact_type)

    class Meta:
        db_table = "list_of_contact_type"


class list_of_country(models.Model):
    country_id = models.CharField(primary_key=True, max_length=2)
    country_name = models.CharField(max_length=50)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.country_name)

    class Meta:
        db_table = "list_of_country"


class list_of_country_region(models.Model):
    region_id = models.AutoField(primary_key=True)
    country = models.ForeignKey(
        'list_of_country',
        on_delete=models.CASCADE,
    )
    region_name = models.CharField(max_length=150)
    region_type = models.CharField(
        max_length=80,
        null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='%(class)s_change_user', blank=True,
                                    null=True)
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.region_name)

    class Meta:
        db_table = "list_of_country_region"


class list_of_lead_source(models.Model):
    lead_source_id = models.AutoField(primary_key=True)
    lead_source_description = models.CharField(max_length=20)
    list_order = models.IntegerField(unique=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.lead_source_description)

    class Meta:
        db_table = "list_of_lead_source"


class list_of_opportunity_stage(models.Model):
    opportunity_stage_id = models.AutoField(primary_key=True)
    opportunity_stage_description = models.CharField(max_length=50)
    probability_success = models.DecimalField(
        max_digits=3,
        decimal_places=0,
    )
    list_order = models.IntegerField(unique=True)
    opportunity_closed = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.opportunity_stage_description)

    class Meta:
        db_table = "list_of_opportunity_stage"
        ordering = ['list_order']


class list_of_quote_stage(models.Model):
    quote_stage_id = models.AutoField(primary_key=True)
    quote_stage = models.CharField(
        max_length=50,
        unique=True,
    )

    is_invoice = models.BooleanField(
        default=False,
    )
    quote_closed = models.BooleanField(
        default=False,
    )
    sort_order = models.IntegerField(unique=True, auto_created=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.quote_stage)

    class Meta:
        db_table = "list_of_quote_stage"


class list_of_requirement_item_status(models.Model):
    requirement_item_status_id = models.AutoField(primary_key=True)
    requirement_item_status = models.CharField(
        max_length=100,
    )
    status_is_closed = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_status)

    class Meta:
        db_table = "list_of_requirement_item_status"


class list_of_requirement_item_type(models.Model):
    requirement_item_type_id = models.AutoField(primary_key=True)
    requirement_item_type = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_type)

    class Meta:
        db_table = "list_of_requirement_item_type"


class list_of_requirement_status(models.Model):
    requirement_status_id = models.AutoField(primary_key=True)
    requirement_status = models.CharField(
        max_length=50,
    )
    requirement_status_is_closed = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_status)

    class Meta:
        db_table = "list_of_requirement_status"


class list_of_requirement_type(models.Model):
    requirement_type_id = models.AutoField(primary_key=True)
    requirement_type = models.CharField(
        max_length=100,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_type)

    class Meta:
        db_table = "list_of_requirement_type"


class list_of_tax(models.Model):
    tax_id = models.AutoField(primary_key=True)
    tax_amount = models.DecimalField(
        max_digits=6,
        decimal_places=4,
    )
    tax_description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )  # Incase the customer wants to place a name against the tax
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True,
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.tax_amount)  # No need to encode as it is a decimal point

    class Meta:
        db_table = "list_of_tax"


class list_of_title(models.Model):
    title_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.title)

    class Meta:
        db_table = "list_of_title"


class nearbeach_option(models.Model):
    """
    This table will store the options for NearBeach. These options will have a new row each time a new option is created
    There does not need to be a is_deleted function
    """
    nearbeach_option_id = models.AutoField(primary_key=True)
    story_point_hour_min = models.IntegerField(
        default=4,
    )
    story_point_hour_max = models.IntegerField(
        default=10,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user',
        blank=True,
        null=True
    )

    def __str__(self):
        return str(self.nearbeach_option_id)

    class Meta:
        db_table = "nearbeach_option"


class object_assignment(models.Model):
    """
    Object permissions is the centralised permissions for all objects
    - Opportunity
    - Quote
    - Requirement
    - Project
    - Task
    - Kanban board
    - Request for change

    These permission are only "ACCESS" permissions. The user/group's over riding permissions determine if the user
    can add, edit etc.
    """
    object_assignment_id = models.AutoField(primary_key=True)
    assigned_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_assigned_user',
        null=True,
        blank=True,
    )
    group_id = models.ForeignKey(
        'group',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    opportunity = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    quote = models.ForeignKey(
        'quote',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        'requirement',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        'requirement_item',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    kanban_board = models.ForeignKey(
        'kanban_board',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        'request_for_change',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    whiteboard = models.ForeignKey(
        'whiteboard',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "object_assignment"


class object_note(models.Model):
    object_note_id = models.AutoField(primary_key=True)
    object_note = models.TextField(
        blank=False,
        null=False,
    )
    kanban_card = models.ForeignKey(
        'kanban_card',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    opportunity = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    quote = models.ForeignKey(
        'quote',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement = models.ForeignKey(
        'requirement',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    requirement_item = models.ForeignKey(
        'requirement_item',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    request_for_change = models.ForeignKey(
        'request_for_change',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "object_note"


class opportunity(models.Model):
    opportunity_id = models.AutoField(primary_key=True)
    opportunity_name = models.CharField(max_length=255)
    opportunity_description = models.TextField('oppertunity_description')
    currency = models.ForeignKey(
        'list_of_currency',
        on_delete=models.CASCADE,
    )
    opportunity_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )  # Turn into a number widget
    amount_type = models.ForeignKey(
        'list_of_amount_type',
        on_delete=models.CASCADE
    )
    opportunity_expected_close_date = models.DateTimeField()
    opportunity_stage = models.ForeignKey(
        'list_of_opportunity_stage',
        on_delete=models.CASCADE
    )
    opportunity_success_probability = models.IntegerField()  # Between 0% and 100%
    lead_source = models.ForeignKey(
        'list_of_lead_source',
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "opportunities"


"""
class opportunity_connection(models.Model):
    opportunity_connection_id = models.AutoField(primary_key=True)
    opportunity=models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
    )
    customer=models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation=models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "organisation_connection"
        """


class organisation(models.Model):
    organisation_id = models.AutoField(primary_key=True)
    organisation_name = models.CharField(max_length=255)
    organisation_website = models.CharField(max_length=50)
    organisation_email = models.CharField(max_length=100)
    organisation_profile_picture = models.ImageField(
        blank=True,
        null=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.organisation_name)

    class Meta:
        db_table = "organisation"


class permission_set_manager(models.Manager):
    def get_by_natural_key(
            self,
            permission_set_id,
            permission_set_name,
            administration_assign_user_to_group,
            administration_create_group,
            administration_create_permission_set,
            administration_create_user,
            bug_client,
            customer,
            email,
            kanban,
            kanban_card,
            organisation,
            project,
            request_for_change,
            requirement,
            task,
            document,
            kanban_comment,
            project_history,
            task_history,
    ):
        return self.get(
            permission_set_id=permission_set_id,
            permission_set_name=permission_set_name,
            administration_assign_user_to_group=administration_assign_user_to_group,
            administration_create_group=administration_create_group,
            administration_create_permission_set=administration_create_permission_set,
            administration_create_user=administration_create_user,
            bug=bug,
            bug_client=bug_client,
            customer=customer,
            email=email,
            kanban=kanban,
            kanban_card=kanban_card,
            opportunity=opportunity,
            organisation=organisation,
            project=project,
            quote=quote,
            request_for_change=request_for_change,
            requirement=requirement,
            task=task,
            document=document,
            kanban_comment=kanban_comment,
            project_history=project_history,
            task_history=task_history,
        )


class permission_set(models.Model):
    objects = permission_set_manager()

    permission_set_id = models.AutoField(primary_key=True)
    permission_set_name = models.CharField(
        max_length=255,
        # unique=True, #issue when we delete previous permission sets
    )
    # ADMINISTRATION PERMISSIONS
    administration_assign_user_to_group = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_group = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_permission_set = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_user = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    bug_client = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    customer = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban_board = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban_card = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    organisation = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    project = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    request_for_change = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    requirement = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0
    )
    task = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    """
    ADDITIVE permission
    ~~~~~~~~~~~~~~~~~~~~
    Designed to add on extra abilities to those user who have "READ ONLY" for certain modules.
    If a user has the ability to "EDIT" for any of these modules, then this section does not 
    need to be populated with data.
    """
    document = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    kanban_comment = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    project_history = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    task_history = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def natural_key(self):
        return (
            self.permission_set_id,  # 0
            self.permission_set_name,  # 1
            self.administration_assign_user_to_group,  # 2
            self.administration_create_group,  # 3
            self.administration_create_permission_set,  # 4
            self.administration_create_user,  # 5
            self.assign_campus_to_customer,  # 6
            self.associate_project_and_task,  # 7
            self.customer,  # 8
            self.opportunity,  # 11
            self.organisation,  # 12
            self.organisation_campus,  # 13
            self.project,  # 14
            self.requirement,  # 15
            self.requirement_link,  # 16
            self.task,  # 17
            self.document,  # 18
            self.contact_history,  # 19
            self.project_history,  # 20
            self.task_history,  # 21
        )

    def __str__(self):
        return str(self.permission_set_name)

    class Meta:
        db_table = "permission_set"


class project(models.Model):
    project_id = models.AutoField(primary_key=True)
    project_name = models.CharField(max_length=255)
    project_description = models.TextField('project_description')
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    # Only fill this field out if there are no organisation
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    project_start_date = models.DateTimeField()
    project_end_date = models.DateTimeField()
    project_status = models.CharField(
        max_length=15,
        choices=PROJECT_STATUS_CHOICE,
        default='New'
    )
    project_story_point_min = models.IntegerField(default=1)
    project_story_point_max = models.IntegerField(default=4)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.project_name)

    class Meta:
        db_table = "project"


class project_customer(models.Model):
    project_customer_id = models.AutoField(primary_key=True)
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
    )
    customer_description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "project_customer"


"""
class project_group(models.Model):
    project_id = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
    )
    group_id = models.ForeignKey(
        'group',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "project_group"
"""

"""
class project_history(models.Model):
    project_history_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True
    )
    user_infomation = models.CharField(max_length=255)
    project_history = models.TextField('project_history')
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.project_id)

    class Meta:
        db_table = "project_history"
"""

"""
class project_opportunity(models.Model):
    project_opprtunity_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
    )
    opportunity_id = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
    )
    opportunity_description = models.CharField(
        max_length=255,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "project_opportunity"
"""

"""
class project_stage(models.Model):
    project_stage_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
    )
    stage_id = models.ForeignKey(
        'stage',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "project_stage"
"""

"""
class project_task(models.Model):
    project_task_id = models.AutoField(primary_key=True)
    project_id = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        db_column='project_id'
    )
    task_id = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        db_column='task_id'
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "project_task"
"""


class quote(models.Model):
    quote_id = models.AutoField(primary_key=True)
    quote_uuid = models.UUIDField(
        default=uuid.uuid4,
        editable=False,
        primary_key=False,
        unique=True,
    )
    quote_title = models.CharField(max_length=255)
    quote_valid_till = models.DateTimeField()
    quote_stage = models.ForeignKey(
        'list_of_quote_stage',
        on_delete=models.CASCADE,
    )
    quote_billing_address = models.ForeignKey(
        'campus',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    is_invoice = models.BooleanField(
        default=False,
    )
    """
    quote_approval_status_id = models.CharField(
        max_length=10,
        choices=QUOTE_APPROVAL_STATUS,
        default='DRAFT',
    )
    """
    quote_terms = models.TextField(
        null=True,
        blank=True,
    )
    customer_notes = models.TextField(
        null=True,
        blank=True,
    )
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        db_column='project_id',
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        db_column='task_id',
        null=True,
        blank=True,
    )
    opportunity = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
        db_column='opportunity_id',
        null=True,
        blank=True,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        db_column='customer_id',
        null=True,
        blank=True,
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        db_column='organisation_id',
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.quote_title)

    class Meta:
        db_table = "quote"


class request_for_change(models.Model):
    """
    Due to the long and complicated name, request for change will be shortened to rfc for ALL fields.
    """
    rfc_id = models.AutoField(primary_key=True)
    rfc_title = models.CharField(
        max_length=255,
    )
    rfc_summary = models.TextField(
        'rfc_summary'
    )
    rfc_type = models.IntegerField(
        choices=RFC_TYPE,
    )
    rfc_implementation_start_date = models.DateTimeField()
    rfc_implementation_end_date = models.DateTimeField()
    rfc_implementation_release_date = models.DateTimeField()
    rfc_version_number = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )
    rfc_status = models.IntegerField(
        choices=RFC_STATUS,
    )
    rfc_lead = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='rfc_lead',

    )
    rfc_priority = models.IntegerField(
        choices=RFC_PRIORITY,
        default=1,
    )
    rfc_risk = models.IntegerField(
        choices=RFC_RISK,
        default=1,
    )
    rfc_impact = models.IntegerField(
        choices=RFC_IMPACT,
        default=1,
    )
    rfc_risk_and_impact_analysis = models.TextField(
        'rfc_risk_and_impact_analysis',
    )
    rfc_implementation_plan = models.TextField(
        'rfc_implementation_plan',
    )
    rfc_backout_plan = models.TextField(
        'rfc_backout_plan',
    )
    rfc_test_plan = models.TextField(
        'rfc_test_plan',
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.rfc_title)

    class Meta:
        db_table = "request_for_change"


class request_for_change_group_approval(models.Model):
    rfc_group_approval_id = models.AutoField(primary_key=True)
    rfc = models.ForeignKey(
        'request_for_change',
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        'group',
        on_delete=models.CASCADE,
    )
    approval = models.IntegerField(
        choices=RFC_APPROVAL,
        default=1,  # Waiting
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.approval)

    class Meta:
        db_table = "request_for_change_group_approval"


class request_for_change_note(models.Model):
    rfc_note_id = models.AutoField(primary_key=True)
    rfc_note = models.TextField(
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.rfc_note)

    class Meta:
        db_table = "request_for_change_note"


class request_for_change_stakeholder(models.Model):
    """
    This model will store all the stakeholders for those request for changes. The stakeholders could be an organisation
    OR a customer.

    rfc = request for change. It is shortened to make it easier for the programmer.
    """
    rfc_stakeholder_id = models.AutoField(primary_key=True)
    request_for_change = models.ForeignKey(
        'request_for_change',
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "request_for_change_stakeholder"


class requirement(models.Model):
    requirement_id = models.AutoField(primary_key=True)
    requirement_title = models.CharField(
        max_length=255,
    )
    requirement_scope = models.TextField(
        null=True,
        blank=True,
    )
    requirement_type = models.ForeignKey(
        'list_of_requirement_type',
        on_delete=models.CASCADE,
    )
    requirement_status = models.ForeignKey(
        'list_of_requirement_status',
        on_delete=models.CASCADE,
    )
    requirement_story_point_min = models.IntegerField(default=1)
    requirement_story_point_max = models.IntegerField(default=4)
    organisation = models.ForeignKey(
        organisation,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_title)

    class Meta:
        db_table = "requirement"


class requirement_customer(models.Model):
    requirement_customer_id = models.AutoField(primary_key=True)
    requirement = models.ForeignKey(
        requirement,
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        customer,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_customer_id)

    class Meta:
        db_table = "requirement_customer"


class requirement_item(models.Model):
    requirement_item_id = models.AutoField(primary_key=True)
    requirement = models.ForeignKey(
        'requirement',
        on_delete=models.CASCADE,
    )
    requirement_item_title = models.CharField(max_length=255)
    requirement_item_scope = models.TextField(
        null=True,
        blank=True,
    )
    requirement_item_status = models.ForeignKey(
        'list_of_requirement_item_status',
        on_delete=models.CASCADE,
    )
    requirement_item_type = models.ForeignKey(
        'list_of_requirement_item_type',
        on_delete=models.CASCADE,
    )
    ri_story_point_min = models.IntegerField(default=4)
    ri_story_point_max = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.requirement_item_title)

    class Meta:
        db_table = "requirement_item"


class tag(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(
        max_length=50,
        unique=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.tag_name)

    class Meta:
        db_table = "tag"


class tag_assignment(models.Model):
    tag_assignment_id = models.AutoField(primary_key=True)
    tag = models.ForeignKey(
        tag,
        on_delete=models.CASCADE,
    )
    project = models.ForeignKey(
        project,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    opportunity = models.ForeignKey(
        opportunity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement = models.ForeignKey(
        requirement,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "tag_assignment"


class task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_short_description = models.CharField(max_length=255)
    task_long_description = models.TextField()
    organisation = models.ForeignKey(
        'organisation',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task_start_date = models.DateTimeField()
    task_end_date = models.DateTimeField()
    task_assigned_to = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
    )
    task_status = models.CharField(
        max_length=15,
        choices=PROJECT_STATUS_CHOICE,
        default='New'
    )
    task_story_point_min = models.IntegerField(default=4)
    task_story_point_max = models.IntegerField(default=10)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    creation_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_creation_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return str(self.task_short_description)

    class Meta:
        db_table = "task"


class task_action(models.Model):
    task_action_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
    )
    task_action = models.TextField()
    submitted_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_action"


class task_customer(models.Model):
    task_customer_id = models.AutoField(primary_key=True)
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
    )
    customer = models.ForeignKey(
        'customer',
        on_delete=models.CASCADE,
    )
    customer_description = models.CharField(
        max_length=155,
        null=True,
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_customer"


"""
class task_group(models.Model):
    task_group_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
    )
    group_id = models.ForeignKey(
        'group',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_group"
"""

"""
class task_history(models.Model):
    task_history_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
    )
    user_id = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    user_infomation = models.CharField(max_length=255)
    task_history = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_history"
"""

"""
class task_opportunity(models.Model):
    task_opportunity_id = models.AutoField(primary_key=True)
    task_id = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
    )
    opportunity_id = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "task_opportunity"
"""


class timesheet(models.Model):
    timesheet_id = models.AutoField(primary_key=True)
    timesheet_description = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    timesheet_date = models.DateField()
    timesheet_start_time = models.TimeField()
    timesheet_end_time = models.TimeField()
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    requirement_item = models.ForeignKey(
        'requirement_item',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    # Doubles up as the user inputting the time
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "timesheet"


class to_do(models.Model):
    to_do_id = models.AutoField(primary_key=True)
    to_do = models.CharField(
        max_length=255,
    )
    to_do_completed = models.BooleanField(default=False)
    project = models.ForeignKey(
        'project',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    task = models.ForeignKey(
        'task',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    opportunity = models.ForeignKey(
        'opportunity',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "to_do"


class user_group(models.Model):
    user_group_id = models.AutoField(primary_key=True)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    group = models.ForeignKey(
        'group',
        on_delete=models.CASCADE,
    )
    permission_set = models.ForeignKey(
        'permission_set',
        on_delete=models.CASCADE,
    )
    report_to = models.ForeignKey(
        User,
        related_name='report_to',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    group_leader = models.BooleanField(
        default=False,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    class Meta:
        db_table = "user_group"


class user_want(models.Model):
    user_want_id = models.AutoField(
        primary_key=True,
    )
    want_choice = models.CharField(
        max_length=50,
        choices=WANT_CHOICE,
    )
    want_choice_text = models.CharField(
        max_length=50,
    )
    want_skill = models.CharField(
        max_length=50,
        choices=SKILL_CHOICE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.want_choice_text

    class Meta:
        db_table = "user_want"


class user_weblink(models.Model):
    user_weblink_id = models.AutoField(primary_key=True)
    user_weblink_url = models.URLField(max_length=255)
    user_weblink_source = models.CharField(
        max_length=50,
        choices=WEBSITE_SOURCE,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.user_weblinks_url

    class Meta:
        db_table = "user_weblink"


class whiteboard(models.Model):
    whiteboard_id = models.AutoField(primary_key=True)
    whiteboard_title = models.CharField(max_length=255)
    whiteboard_xml = models.TextField(
        null=True,
        blank=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    change_user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='%(class)s_change_user'
    )
    is_deleted = models.BooleanField(
        default=False,
    )

    def __str__(self):
        return self.whiteboard_title

    class Meta:
        db_table = "whiteboard"
