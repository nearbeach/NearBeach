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
		return self.folder_description.encode('utf8')

	class Meta:
		db_table="folder"


class groups(models.Model):
	group_id=models.AutoField(primary_key=True)
	group_name=models.CharField(
		max_length=50,
		unique=True
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
		return self.group_name.encode('utf8')
	
	class Meta:
		db_table="groups"

class group_permissions(models.Model):
	role=models.CharField(max_length=15)
	
	def __str__(self):
		return self.role.encode('utf8')
	
	class Meta:
		db_table="group_permissions"


class list_of_amount_type(models.Model):
	amount_type_id=models.AutoField(primary_key=True)
	amount_type_description=models.CharField(max_length=20)
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
		return self.amount_type_description.encode('utf8')

	class Meta:
		db_table="list_of_amount_type"
		ordering=['list_order']




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
	contact_type=models.CharField(max_length=10)
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


class list_of_taxes(models.Model):
	tax_id = models.AutoField(primary_key=True)
	tax_amount=models.DecimalField(
		max_digits=4,
		decimal_places=2,
	)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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
		on_delete=models.CASCADE
	)
	customer_id=models.ForeignKey(
		'customers',
		on_delete=models.CASCADE,
		null=True,
		blank=True
	)
	currency_id=models.ForeignKey(
		'list_of_currency',
		on_delete=models.CASCADE
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
		db_table="opportunity_permission"



class opportunity_next_step(models.Model):
	opportunity_id=models.ForeignKey(
		'opportunity',
		on_delete=models.CASCADE
	)
	next_step_description=models.CharField(max_length=255)
	next_step_completed=models.BooleanField(default=False)
	date_created=models.DateTimeField(auto_now_add=True)
	date_modified=models.DateTimeField(auto_now=True)
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
		db_table='opportunity_next_step'


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
	project_tasks=models.AutoField(primary_key=True)
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
		max_digits=4,
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
		max_digits=3,
		decimal_places=2,
		validators=[MaxValueValidator(100), MinValueValidator(0)]  # Could I use this for the money too? :D
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
		blank=True
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
	submitted_by=models.ForeignKey(User,)
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


class user_groups(models.Model):
	username=models.ForeignKey(User,)
	group_id=models.ForeignKey(
		'groups',
		on_delete=models.CASCADE,
	)
	user_group_permission=models.ForeignKey(
		'group_permissions',
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
