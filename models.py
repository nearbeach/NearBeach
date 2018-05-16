from __future__ import unicode_literals
from django.db import models, connection
from .private_media import *
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
import uuid

#ENUM choices
DISCOUNT_CHOICE=(
	('Percentage','Percentage'),
	('Amount','Amount'),
)

IS_DELETED_CHOICE=(
	('TRUE','TRUE'),
	('FALSE','FALSE'),
)

PERMISSION_LEVEL=(
	(0, 'No Permission'),
	(1, 'Read Only'),
	(2, 'Edit Only'),
	(3, 'Add and Edit'),
	(4, 'Full Permission'),
)

PERMISSION_BOOLEAN=(
	(0, 'No Permission'),
	(1, 'Has Permission'),
)

PRODUCT_OR_SERVICE=(
	('Product','Product'),
	('Service','Service'),
)

PROJECT_STATUS_CHOICE=(
	('New','New'),
	('Open','Open'),
	('Resolved','Resolved'),
	('Closed','Closed'),
)

QUOTE_APPROVAL_STATUS=(
	('REJECTED','REJECTED'),
	('DRAFT','DRAFT'),
	('APPROVED','APPROVED'),
)

#List of tables - in alphabetical order
class assigned_users(models.Model):
	assigned_users_id=models.AutoField(primary_key=True)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	task_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	opportunity_id=models.ForeignKey(
		'opportunity',
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table="assigned_users"


"""
Contact History is a simple form that users will fill out every time they
have some form of contact with the customer. This table will store both
contact history for Customers and Organisations. The customer field in
this instance is not required, and implies that the contact history is 
applied to the organisation. The organisation field will fill out automatically
when a user applies it to a customer. :)
"""
class contact_history(models.Model):
	contact_history_id=models.AutoField(primary_key=True)
	organisations_id=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	contact_type=models.ForeignKey(
		'list_of_contact_types',
		on_delete=models.CASCADE,
	)
	contact_date=models.DateTimeField()
	contact_history=models.TextField()
	document_key=models.ForeignKey(
		'documents',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)


	class Meta:
		db_table="contact_history"


class bug(models.Model):
	bug_id=models.AutoField(primary_key=True)
	bug_client=models.ForeignKey(
		'bug_client',
		on_delete=models.CASCADE,
	)
	bug_code=models.CharField(max_length=255) #Just stores the code of the bug
	bug_description=models.TextField()
	bug_status=models.CharField(max_length=50) #Updated manually?
	project=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	tasks=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	requirements=models.ForeignKey(
		'requirements',
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.bug_description.encode('utf8')

	class Meta:
		db_table = "bug"




class bug_client(models.Model):
	bug_client_id=models.AutoField(primary_key=True)
	bug_client_name=models.CharField(max_length=50)
	list_of_bug_client=models.ForeignKey(
		'list_of_bug_client',
		on_delete=models.CASCADE,
	)
	bug_client_url=models.URLField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey \
		(User,
		 on_delete=models.CASCADE,
		 related_name='%(class)s_change_user',
		 )
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.bug_client_name.encode('utf8')

	class Meta:
		db_table = "bug_client"



class costs(models.Model):
	cost_id=models.AutoField(primary_key=True)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	task_id=models.ForeignKey(
		'tasks', 
		on_delete=models.CASCADE, 
		blank=True, 
		null=True
	)
	cost_description=models.CharField(max_length=255, )
	cost_amount=models.DecimalField(
		max_digits=19, 
		decimal_places=2
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey\
		(User, 
		 on_delete=models.CASCADE,
		 related_name='%(class)s_change_user',
	)
	is_deleted=models.CharField(
		max_length=5, 
		choices=IS_DELETED_CHOICE, 
		default='FALSE'
	)
	def __str__(self):
		return '$' + str(self.cost_amount)

	class Meta:
		db_table="costs"


class customers(models.Model):
	customer_id=models.AutoField(primary_key=True)
	customer_title=models.ForeignKey(
		'list_of_titles', 
		on_delete=models.CASCADE,
	)
	customer_first_name=models.CharField(max_length=50)
	customer_last_name=models.CharField(max_length=50)
	customer_email=models.CharField(max_length=200)
	customer_profile_picture=models.ImageField(
		blank=True,
		null=True,
		upload_to='profile_pictures'
	)
	organisations_id=models.ForeignKey(
		'organisations', 
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User, 
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5, 
		choices=IS_DELETED_CHOICE, 
		default='FALSE'
	)
	def __str__(self):
		return str(self.customer_id) + ' - ' + self.customer_first_name.encode('utf8') + ' ' + self.customer_last_name.encode('utf8')
	
	class Meta:
		db_table="customers"

class customers_campus(models.Model):
	customers_campus_id=models.AutoField(primary_key=True)
	customer_id=models.ForeignKey(
		'customers', 
		on_delete=models.CASCADE,
	)
	campus_id=models.ForeignKey(
		'organisations_campus', 
		on_delete=models.CASCADE,
	)
	customer_phone=models.CharField(max_length=11)
	customer_fax=models.CharField(max_length=11)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User, 
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5, 
		choices=IS_DELETED_CHOICE, 
		default='FALSE'
	)
	class Meta:
		db_table="customers_campus"



class documents(models.Model):
	document_key=models.UUIDField(
		default=uuid.uuid4,
		editable=False,
		primary_key=True,
	)
	document_description=models.CharField(max_length=255)
	document_url_location=models.TextField(
		# Contains URLS
		null=True,
		blank=True,
	)
	document=models.FileField(
		blank=True,
		null=True,
		storage=File_Storage(),
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table="documents"

	def __str__(self):
		return self.document_description


class documents_folder(models.Model):
	documents_folder_id=models.AutoField(primary_key=True)
	document_key=models.ForeignKey(
		'documents',
		on_delete=models.CASCADE,
	)
	folder_id=models.ForeignKey(
		'folders',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)


	class Meta:
		db_table="documents_folder"



class document_permissions(models.Model):
	document_permisssions_id=models.AutoField(primary_key=True)
	document_key=models.ForeignKey(
		'documents',
		on_delete=models.CASCADE,
	)
	project_id=models.ForeignKey(
		'project',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	task_id=models.ForeignKey(
		'tasks',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	organisations_id=models.ForeignKey(
		'organisations',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	customer_id=models.ForeignKey(
		'customers',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	opportunity_id=models.ForeignKey(
		'opportunity',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	requirements=models.ForeignKey(
		'requirements',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	requirement_item=models.ForeignKey(
		'requirement_item',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="document_permissions"


class email_contact(models.Model):
	email_contact_id=models.AutoField(primary_key=True)
	email_content=models.ForeignKey(
		'email_content',
		on_delete=models.CASCADE,
	)
	to_customers = models.ForeignKey(
		'customers',
		related_name='%(class)s_to_customers',
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	cc_customers=models.ForeignKey(
		'customers',
		related_name='%(class)s_cc_customers',
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	bcc_customers=models.ForeignKey(
		'customers',
		related_name='%(class)s_bcc_customers',
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	organisations=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="email_contact"


class email_content(models.Model):
	email_content_id=models.AutoField(primary_key=True)
	email_subject=models.CharField(max_length=255)
	email_content=models.TextField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table = "email_content"


class folders(models.Model):
	folder_id=models.AutoField(primary_key=True)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	task_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		blank=True,
		null=True
	)
	folder_description=models.CharField(max_length=255)
	parent_folder_id=models.ForeignKey(
		'self',
		blank=True,
		null=True,
		on_delete=models.CASCADE
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)
	def __str__(self):
		return self.folder_description.encode('utf8')

	class Meta:
		db_table="folder"


class groups(models.Model):
	group_id = models.AutoField(primary_key=True)
	group_name = models.CharField(
		max_length=50,
		unique=True
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def natural_key(self):
		return (
			self.group_id,
			self.group_name
		)

	def __str__(self):
		return self.group_name.encode('utf8')

	class Meta:
		db_table = "groups"


class groups_manager(models.Manager):
	def get_by_natural_key(
			self,
			group_id,
			group_name
	):
		return self.get(
			group_id=group_id,
			group_name=group_name
		)

class group_permissions(models.Model):
	group_permissions_id=models.AutoField(primary_key=True)
	permission_set=models.ForeignKey(
		'permission_set',
		on_delete=models.CASCADE,
	)
	groups = models.ForeignKey(
		'groups',
		on_delete=models.CASCADE
	)

	def __str__(self):
		return str(self.permission_set)
	
	class Meta:
		db_table="group_permissions"


class kanban_board(models.Model):
	kanban_board_id=models.AutoField(primary_key=True)
	kanban_board_name=models.CharField(max_length=255)
	requirements=models.ForeignKey(
		'requirements',
		null=True,
		blank=True,
		on_delete=models.CASCADE,
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table = "kanban_board"

	def __str__(self):
		return self.kanban_board_name


class kanban_card(models.Model):
	kanban_card_id=models.AutoField(primary_key=True)
	kanban_card_text=models.CharField(max_length=255)
	kanban_card_sort_number=models.IntegerField()
	kanban_level=models.ForeignKey(
		'kanban_level',
		on_delete=models.CASCADE,
	)
	kanban_column=models.ForeignKey(
		'kanban_column',
		on_delete=models.CASCADE,
	)
	kanban_board=models.ForeignKey(
		'kanban_board',
		on_delete=models.CASCADE,
	)
	project=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	tasks=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	requirements=models.ForeignKey(
		'requirements',
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table = "kanban_card"

	def __str__(self):
		return self.kanban_card_text


class kanban_column(models.Model):
	kanban_column_id=models.AutoField(primary_key=True)
	kanban_column_name=models.CharField(max_length=255)
	kanban_column_sort_number=models.IntegerField()
	kanban_board=models.ForeignKey(
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table = "kanban_column"

	def __str__(self):
		return self.kanban_column_name


class kanban_comment(models.Model):
	kanban_comment_id=models.AutoField(primary_key=True)
	kanban_comment=models.TextField()
	kanban_board=models.ForeignKey(
		'kanban_board',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	kanban_card=models.ForeignKey(
		'kanban_card',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		null=True
	)
	user_infomation = models.CharField(max_length=255)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table = "kanban_comment"

	def __str__(self):
		return self.kanban_comment


class kanban_level(models.Model):
	kanban_level_id=models.AutoField(primary_key=True)
	kanban_level_name=models.CharField(max_length=255)
	kanban_level_sort_number=models.IntegerField()
	kanban_board=models.ForeignKey(
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)

	class Meta:
		db_table = "kanban_level"

	def __str__(self):
		return self.kanban_level_name





class list_of_amount_type(models.Model):
	amount_type_id=models.AutoField(primary_key=True)
	amount_type_description=models.CharField(max_length=20)
	list_order=models.IntegerField(unique=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.amount_type_description.encode('utf8')

	class Meta:
		db_table="list_of_amount_type"
		ordering=['list_order']


class list_of_bug_client(models.Model):
	list_of_bug_client_id=models.AutoField(primary_key=True)
	bug_client_name=models.CharField(max_length=50)
	bug_client_api_url=models.CharField(max_length=255)

	#The different API commands
	api_open_bugs=models.CharField(max_length=255)	#Find all open bugs
	api_search_bugs=models.CharField(max_length=255) #Search command
	api_bug=models.CharField(max_length=255) #Get that particular bug information - direct link to bug

	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.bug_client_name.encode('utf8')

	class Meta:
		db_table="list_of_bug_client"



class list_of_currency(models.Model):
	currency_id=models.AutoField(primary_key=True)
	currency_description=models.CharField(max_length=20)
	currency_short_description=models.CharField(max_length=4)
	list_order=models.IntegerField(unique=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.currency_description.encode('utf8')

	class Meta:
		db_table="list_of_currency"


class list_of_contact_types(models.Model):
	contact_type_id=models.AutoField(primary_key=True)
	contact_type=models.CharField(max_length=50)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.contact_type.encode('utf8')

	class Meta:
		db_table="list_of_contact_types"


class list_of_countries(models.Model):
	country_id=models.CharField(primary_key=True, max_length=2)
	country_name=models.CharField(max_length=50)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.country_name.encode('utf8')
	
	class Meta:
		db_table="list_of_countries"


class list_of_countries_regions(models.Model):
	region_id=models.AutoField(primary_key=True)
	country_id=models.ForeignKey(
		'list_of_countries',
		on_delete=models.CASCADE,
	)
	region_name=models.CharField(max_length=150)
	region_type=models.CharField(
		max_length=80,
		null=True
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(User, on_delete=models.CASCADE,related_name='%(class)s_change_user',blank=True,null=True)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.region_name.encode('utf8')
	
	class Meta:
		db_table="list_of_countries_regions"




class list_of_lead_source(models.Model):
	lead_source_id=models.AutoField(primary_key=True)
	lead_source_description=models.CharField(max_length=20)
	list_order=models.IntegerField(unique=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.lead_source_description.encode('utf8')

	class Meta:
		db_table="list_of_lead_source"




class list_of_opportunity_stage(models.Model):
	opportunity_stage_id=models.AutoField(primary_key=True)
	opportunity_stage_description=models.CharField(max_length=50)
	probability_success=models.DecimalField(
		max_digits=3,
		decimal_places=0,
	)
	list_order=models.IntegerField(unique=True)
	opportunity_closed=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.opportunity_stage_description.encode('utf8')

	class Meta:
		db_table="list_of_opportunity_stage"
		ordering=['list_order']




class list_of_quote_stages(models.Model):
	quote_stages_id=models.AutoField(primary_key=True)
	quote_stage=models.CharField(
		max_length=50,
		unique=True,
	)
	"""
	For the quote stages; if the quote is still a quote, then the dropdown box
	will only show those who are NOT an is_invoice=TRUE. However if the quote
	has been turned into an INVOICE, then the dropdown box will show those
	is_invoice=TRUE
	"""
	is_invoice=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)
	quote_closed=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)
	sort_order = models.IntegerField(unique=True,auto_created=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.quote_stage.encode('utf8')

	class Meta:
		db_table="list_of_quote_stages"




class list_of_requirement_item_status(models.Model):
	requirement_item_status_id=models.AutoField(primary_key=True)
	requirement_item_status = models.CharField(
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.requirement_item_status)

	class Meta:
		db_table = "list_of_requirement_item_status"


class list_of_requirement_item_type(models.Model):
	requirement_item_type_id=models.AutoField(primary_key=True)
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.requirement_item_type)

	class Meta:
		db_table = "list_of_requirement_item_type"



class list_of_requirement_status(models.Model):
	requirement_status_id=models.AutoField(primary_key=True)
	requirement_status=models.CharField(
		max_length=50,
	)
	requirement_status_is_closed=models.CharField(
		max_length=10,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.requirement_status)

	class Meta:
		db_table = "list_of_requirement_status"





class list_of_requirement_type(models.Model):
	requirement_type_id = models.AutoField(primary_key=True)
	requirement_type=models.CharField(
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.requirement_type)

	class Meta:
		db_table="list_of_requirement_type"




class list_of_taxes(models.Model):
	tax_id = models.AutoField(primary_key=True)
	tax_amount=models.DecimalField(
		max_digits=6,
		decimal_places=4,
	)
	tax_description=models.CharField(
		max_length=50,
		blank=True,
		null=True,
	) #Incase the customer wants to place a name against the tax
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.tax_amount) #No need to encode as it is a decimal point

	class Meta:
		db_table="list_of_taxes"


class list_of_titles(models.Model):
	title_id=models.AutoField(primary_key=True)
	title=models.CharField(max_length=10)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user',
		blank=True,
		null=True
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.title.encode('utf8')
	
	class Meta:
		db_table="list_of_titles"

class opportunity(models.Model):
	opportunity_id=models.AutoField(primary_key=True)
	opportunity_name=models.CharField(max_length=255)
	opportunity_description=models.TextField()
	organisations_id=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	currency_id=models.ForeignKey(
		'list_of_currency',
		on_delete=models.CASCADE,
	)
	opportunity_amount=models.DecimalField(
		max_digits=12,
		decimal_places=2
	) #Turn into a number widget
	amount_type_id=models.ForeignKey(
		'list_of_amount_type',
		on_delete=models.CASCADE
	)
	opportunity_expected_close_date=models.DateTimeField()
	opportunity_stage_id=models.ForeignKey(
		'list_of_opportunity_stage',
		on_delete=models.CASCADE
	)
	opportunity_success_probability=models.IntegerField() #Between 0% and 100%
	lead_source_id=models.ForeignKey(
		'list_of_lead_source',
		on_delete=models.CASCADE
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	user_id=models.ForeignKey(User, on_delete=models.CASCADE)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="opportunities"


class opportunity_permissions(models.Model):
	opportunity_permissions_id=models.AutoField(primary_key=True)
	opportunity_id=models.ForeignKey(
		'opportunity',
		on_delete=models.CASCADE
	)
	assigned_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_assigned_user',
		null=True,
		blank=True,
	)
	groups_id=models.ForeignKey(
		'groups',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	all_users=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE',
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="opportunity_permission"


class organisations(models.Model):
	organisations_id=models.AutoField(primary_key=True)
	organisation_name=models.CharField(max_length=255)
	organisation_website=models.CharField(max_length=50)
	organisation_email=models.CharField(max_length=100)
	organisation_profile_picture=models.ImageField(
		blank=True,
		null=True
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.organisation_name.encode('utf8')
	
	class Meta:
		db_table="organisations"

	
class organisations_campus(models.Model):
	organisations_campus_id=models.AutoField(primary_key=True)
	organisations_id=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
	)
	campus_nickname=models.CharField(max_length=100)
	campus_phone=models.CharField(
		max_length=11,
		null=True
	)
	campus_fax=models.CharField(
		max_length=11,
		null=True
	)
	campus_address1=models.CharField(
		max_length=255,
		null=True
	)
	campus_address2=models.CharField(
		max_length=255,
		null=True
	)
	campus_address3=models.CharField(
		max_length=255,
		null=True
	)
	campus_suburb=models.CharField(max_length=50)
	campus_region_id=models.ForeignKey(
		'list_of_countries_regions',
		on_delete=models.CASCADE,
	)
	campus_country_id=models.ForeignKey(
		'list_of_countries',
		on_delete=models.CASCADE,
	)
	campus_longitude=models.DecimalField(
		decimal_places=13,
		max_digits=16,
		null=True, #If use has no mapping software, we want to leave this blank
		blank=True,
	)
	campus_latitude=models.DecimalField(
		decimal_places=13,
		max_digits=16,
		null=True, #If use has no mapping software, we want to leave this blank
		blank=True,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.campus_nickname.encode('utf8')
	
	class Meta:
		db_table="organisations_campus"


class permission_set_manager(models.Manager):
    def get_by_natural_key(
            self,
            permission_set_id,
            permission_set_name,
            administration_assign_users_to_groups,
            administration_create_groups,
            administration_create_permission_sets,
            administration_create_users,
            assign_campus_to_customer,
            associate_project_and_tasks,
			bug,
			bug_client,
            customer,
            invoice,
            invoice_product,
			kanban,
			kanban_card,
            opportunity,
            organisation,
            organisation_campus,
            project,
			quote,
			requirement,
			requirement_link,
            task,
			tax,
			documents,
			contact_history,
			kanban_comment,
			project_history,
			task_history,
    ):
        return self.get(
            permission_set_id=permission_set_id,
            permission_set_name=permission_set_name,
            administration_assign_users_to_groups=administration_assign_users_to_groups,
            administration_create_groups=administration_create_groups,
            administration_create_permission_sets=administration_create_permission_sets,
            administration_create_users=administration_create_users,
            assign_campus_to_customer=assign_campus_to_customer,
            associate_project_and_tasks=associate_project_and_tasks,
			bug=bug,
			bug_client=bug_client,
            customer=customer,
            invoice=invoice,
            invoice_product=invoice_product,
			kanban=kanban,
			kanban_card=kanban_card,
            opportunity=opportunity,
            organisation=organisation,
            organisation_campus=organisation_campus,
            project=project,
			quote=quote,
			requirement=requirement,
			requirement_link=requirement_link,
            task=task,
			tax=tax,
			documents=documents,
			contact_history=contact_history,
			kanban_comment=kanban_comment,
			project_history=project_history,
			task_history=task_history,
        )

class permission_set(models.Model):
    objects = permission_set_manager()

    permission_set_id = models.AutoField(primary_key=True)
    permission_set_name = models.CharField(
        max_length=255,
        unique=True,
    )
    # BASELINE PERMISSIONS
    administration_assign_users_to_groups = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_groups = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_permission_sets = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    administration_create_users = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    assign_campus_to_customer = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    associate_project_and_tasks = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    bug=models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0,
	)
    bug_client=models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0,
	)
    invoice = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    invoice_product = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    customer = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    kanban = models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0,
	)
    kanban_card = models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0,
	)
    opportunity = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    organisation = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    organisation_campus = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    project = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
	)
    quote = models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0,
	)
    requirement = models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0
	)
    requirement_link = models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0
	)
    task = models.IntegerField(
        choices=PERMISSION_LEVEL,
        default=0,
    )
    tax = models.IntegerField(
		choices=PERMISSION_LEVEL,
		default=0,
	)
    """
    ADDITIVE PERMISSIONS
    ~~~~~~~~~~~~~~~~~~~~
    Designed to add on extra abilities to those users who have "READ ONLY" for certain modules.
    If a user has the ability to "EDIT" for any of these modules, then this section does not 
    need to be populated with data.
    """
    documents = models.IntegerField(
        choices=PERMISSION_BOOLEAN,
        default=0,
    )
    contact_history = models.IntegerField(
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
    is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

    def natural_key(self):
        return (
            self.permission_set_id, #0
            self.permission_set_name, #1
            self.administration_assign_users_to_groups, #2
            self.administration_create_groups, #3
            self.administration_create_permission_sets, #4
            self.administration_create_users, #5
            self.assign_campus_to_customer, #6
            self.associate_project_and_tasks, #7
            self.customer, #8
            self.invoice, #9
            self.invoice_product, #10
            self.opportunity, #11
            self.organisation, #12
            self.organisation_campus, #13
            self.project, #14
			self.requirement, #15
			self.requirement_link, #16
            self.task, #17
			self.documents, #18
			self.contact_history, #19
			self.project_history, #20
			self.task_history #21
        )

    #class Meta:
    #    unique_together = (('first_name', 'last_name'),)

    def __str__(self):
        return self.permission_set_name.encode('utf8')

    class Meta:
        db_table = "permission_set"



class products_and_services(models.Model):
	"""
	For naming convention, products and services will be shorten to
	just product. The product name contains both products and services
	"""
	product_id=models.AutoField(primary_key=True)
	product_or_service = models.CharField(
		max_length=7,
		choices=PRODUCT_OR_SERVICE,
	)
	product_name=models.CharField(
		max_length=100,
		unique=True, #To stop the user inputting the same product!
	)
	product_part_number=models.CharField(
		max_length=100,
		null=True,
		blank=True,
	)
	product_cost=models.DecimalField(
		max_digits=19,
		decimal_places=2
	)
	product_price=models.DecimalField(
		max_digits=19,
		decimal_places=2,
	)
	product_description=models.TextField(
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.product_name.encode('utf8')

	class Meta:
		db_table = "products_and_services"



class project(models.Model):
	project_id=models.AutoField(primary_key=True)
	project_name=models.CharField(max_length=255)
	project_description=models.TextField()
	organisations_id=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
	)
	project_start_date=models.DateTimeField()
	project_end_date=models.DateTimeField()
	project_status=models.CharField(
		max_length=15,
		choices=PROJECT_STATUS_CHOICE,
		default='New'
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)
	
	def __str__(self):
		return self.project_name.encode('utf8')
	
	class Meta:
		db_table="project"
	
	
class project_customers(models.Model):
	project_customers_id=models.AutoField(primary_key=True)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
	)
	customer_description=models.CharField(
		max_length=255,
		null=True,
		blank=True
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="project_customers"	
	

class project_groups(models.Model):
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
	)
	groups_id=models.ForeignKey(
		'groups',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="project_groups"
		

class project_history(models.Model):
	project_history_id=models.AutoField(primary_key=True)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
	)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		null=True
	)
	user_infomation=models.CharField(max_length=255)
	project_history=models.TextField()
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.region.encode('utf8')
	
	class Meta:
		db_table="project_history"


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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table = "project_opportunity"


class project_stages(models.Model):
	project_stages_id=models.AutoField(primary_key=True)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
	)
	stages_id=models.ForeignKey(
		'stages',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="project_stages"


class project_tasks(models.Model):
	project_tasks_id=models.AutoField(primary_key=True)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		db_column='project_id'
	)
	task_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		db_column='task_id'
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="project_tasks"


class quotes(models.Model):
	quote_id=models.AutoField(primary_key=True)
	quote_title=models.CharField(max_length=255)
	quote_valid_till=models.DateTimeField()
	quote_stage_id = models.ForeignKey(
		'list_of_quote_stages',
		on_delete=models.CASCADE,
	)
	is_invoice=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)
	quote_approval_status_id=models.CharField(
		max_length=10,
		choices=QUOTE_APPROVAL_STATUS,
		default='DRAFT',
	)


	quote_terms=models.TextField(
		null=True,
		blank=True,
	)
	customer_notes=models.TextField(
		null=True,
		blank=True,
	)
	project_id=models.ForeignKey(
		'project',
		on_delete=models.CASCADE,
		db_column='project_id',
		null=True,
		blank=True,
	)
	task_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		db_column='task_id',
		null=True,
		blank=True,
	)
	opportunity_id=models.ForeignKey(
		'opportunity',
		on_delete=models.CASCADE,
		db_column='opportunity_id',
		null=True,
		blank=True,
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
		db_column='customer_id',
		null=True,
		blank=True,
	)
	organisation_id=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
		db_column='organisations_id',
		null=True,
		blank=True,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.quote_title.encode('utf8')

	class Meta:
		db_table="quotes"


class quotes_products_and_services(models.Model):
	quotes_products_and_services_id = models.AutoField(primary_key=True)
	quote=models.ForeignKey(
		'quotes',
		on_delete=models.CASCADE,
	)
	products_and_services=models.ForeignKey(
		'products_and_services',
		on_delete=models.CASCADE,
	)
	#Price of the product BEFORE Discounts
	product_price=models.DecimalField(
		max_digits=19,
		decimal_places=2,
	)
	quantity=models.IntegerField()
	product_description=models.CharField(
		max_length=255,
		blank=True,
		null=True,
	)
	product_cost=models.DecimalField(
		max_digits=19,
		decimal_places=2
	)
	discount_choice=models.CharField(
		max_length=10,
		choices=DISCOUNT_CHOICE,
		default='PERCENTAGE',
	)
	discount_percent=models.DecimalField(
		default=0,
		max_digits=5,
		decimal_places=2,
		validators=[MaxValueValidator(100), MinValueValidator(0)] #Could I use this for the money too? :D
	)
	discount_amount=models.DecimalField(
		default=0,
		max_digits=19,
		decimal_places=2,
		validators=[MaxValueValidator(1000000000), MinValueValidator(0)]  # Could I use this for the money too? :D
	)
	#The price of the product AFTER discounts
	sales_price=models.DecimalField(
		default=0,
		max_digits=19,
		decimal_places=2,
		validators=[MaxValueValidator(1000000000), MinValueValidator(0)]  # Could I use this for the money too? :D
	)
	tax=models.ForeignKey(
		'list_of_taxes',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	tax_amount=models.DecimalField(
		max_digits=19,
		decimal_places=2,
		default=0,
	)
	total=models.DecimalField(
		max_digits=19,
		decimal_places=2,
		validators=[MaxValueValidator(99999999999999999999),MinValueValidator(-99999999999999999999)],
	)
	product_note=models.CharField(
		max_length=255,
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.quotes_products_and_services_id) + "| " + self.product_description.encode('utf8')

	class Meta:
		db_table="quotes_products_and_services"



class quote_responsible_customers(models.Model):
	quote_responsible_customers_id=models.AutoField(primary_key=True)
	quote_id=models.ForeignKey(
		'quotes',
		on_delete=models.CASCADE,
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="quote_responsible_customers"


class requirements(models.Model):
	requirement_id=models.AutoField(primary_key=True)
	requirement_title=models.CharField(
		max_length=255,
	)
	requirement_scope=models.TextField(
		null=True,
		blank=True,
	)
	requirement_type = models.ForeignKey(
		'list_of_requirement_type',
		on_delete=models.CASCADE,
	)
	requirement_status=models.ForeignKey(
		'list_of_requirement_status',
		on_delete=models.CASCADE,
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.requirement_title)


	class Meta:
		db_table="requirements"



class requirement_item(models.Model):
	requirement_item_id = models.AutoField(primary_key=True)
	requirement_id = models.ForeignKey(
		'requirements',
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
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return str(self.requirement_item_title)

	class Meta:
		db_table="requirement_item"



class requirement_item_links(models.Model):
	requirement_item_links_id = models.AutoField(primary_key=True)
	requirement_item = models.ForeignKey(
		'requirement_item',
		on_delete=models.CASCADE,
	)
	project_id = models.ForeignKey(
		'project',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	task_id = models.ForeignKey(
		'tasks',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	organisations_id = models.ForeignKey(
		'organisations',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="requirement_item_permissions"


class requirement_links(models.Model):
	requirement_links_id = models.AutoField(primary_key=True)
	requirements = models.ForeignKey(
		'requirements',
		on_delete=models.CASCADE,
	)
	project_id = models.ForeignKey(
		'project',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	task_id = models.ForeignKey(
		'tasks',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	organisations_id = models.ForeignKey(
		'organisations',
		blank=True,
		null=True,
		on_delete=models.CASCADE,
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	change_user = models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table = "requirement_permissions"



class stages(models.Model):
	stages_id=models.AutoField(primary_key=True)
	group_id=models.ForeignKey(
		'groups',
		on_delete=models.CASCADE,
	)
	stage=models.CharField(max_length=45)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	def __str__(self):
		return self.stage.encode('utf8')
	
	class Meta:
		db_table="stages"
		

class tasks(models.Model):
	tasks_id=models.AutoField(primary_key=True)
	task_short_description=models.CharField(max_length=255)
	task_long_description=models.TextField()
	organisations_id=models.ForeignKey(
		'organisations',
		on_delete=models.CASCADE,
	)
	task_start_date=models.DateTimeField(auto_now=True) 
	task_end_date=models.DateTimeField()
	task_assigned_to=models.ForeignKey(
		User,
		null=True,
		blank=True,
		on_delete=models.CASCADE,
	)
	task_status=models.CharField(
		max_length=15,
		choices=PROJECT_STATUS_CHOICE,
		default='New'
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)
	
	def __str__(self):
		return self.task_short_description.encode('utf8')
	
	class Meta:
		db_table="tasks"

class tasks_actions(models.Model):
	tasks_actions_id=models.AutoField(primary_key=True)
	tasks_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
	)
	task_action=models.TextField()
	submitted_by=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="tasks_actions"	

class tasks_customers(models.Model):
	tasks_customers_id=models.AutoField(primary_key=True)
	tasks_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
	)
	customers_description=models.CharField(
		max_length=155,
		null=True,
		blank=True
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="tasks_customers"
		
class tasks_groups(models.Model):
	tasks_groups_id=models.AutoField(primary_key=True)
	tasks_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
	)
	groups_id=models.ForeignKey(
		'groups',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="tasks_groups"
		
class tasks_history(models.Model):
	tasks_history_id=models.AutoField(primary_key=True)
	tasks_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
	)
	user_id=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	user_infomation=models.CharField(max_length=255)	
	task_history=models.TextField()
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="tasks_history"
		
class tasks_opportunity(models.Model):
	tasks_opportunity_id=models.AutoField(primary_key=True)
	tasks_id=models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
	)
	opportunity_id=models.ForeignKey(
		'opportunity',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="tasks_opportunity"


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
	tasks = models.ForeignKey(
		'tasks',
		on_delete=models.CASCADE,
		null=True,
		blank=True,
	)
	opportunity=models.ForeignKey(
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
	is_deleted = models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table = "to_do"



class user_groups(models.Model):
	user_groups_id=models.AutoField(primary_key=True)
	username=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
	)
	groups=models.ForeignKey(
		'groups',
		on_delete=models.CASCADE,
	)
	permission_set=models.ForeignKey(
		'permission_set',
		on_delete=models.CASCADE,
	)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
	change_user=models.ForeignKey(
		User,
		on_delete=models.CASCADE,
		related_name='%(class)s_change_user'
	)
	is_deleted=models.CharField(
		max_length=5,
		choices=IS_DELETED_CHOICE,
		default='FALSE'
	)

	class Meta:
		db_table="user_groups"	

