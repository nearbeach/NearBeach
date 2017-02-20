from __future__ import unicode_literals

from django.db import models, connection

#Import Django's users
from django.contrib.auth.models import User

#ENUM choices
IS_DELETED_CHOICE = (
	('TRUE','TRUE'),
	('FALSE','FALSE'),
)

PROJECT_STATUS_CHOICE = (
	('New','New'),
	('Open','Open'),
	('Resolved','Resolved'),
	('Closed','Closed'),
)

#List of tables - in alphabetical order
class customers(models.Model):
	customer_id = models.AutoField(primary_key = True)
	customer_title = models.ForeignKey('list_of_titles', on_delete = models.CASCADE,)
	customer_first_name = models.CharField(max_length = 50)
	customer_last_name = models.CharField(max_length = 50)
	customer_email = models.CharField(max_length = 200)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	def __str__(self):
		return str(self.customer_id) + ' - ' + self.customer_first_name + ' ' + self.customer_last_name
	
	class Meta:
		db_table = "customers"

class customers_campus(models.Model):
	customer_id = models.ForeignKey('customers', on_delete = models.CASCADE,)
	campus_id = models.ForeignKey('organisations_campus', on_delete = models.CASCADE,)
	customer_phone = models.CharField(max_length = 11)
	customer_fax = models.CharField(max_length = 11)
	
	class Meta:
		db_table = "customers_campus"

class groups(models.Model):
	group_id = models.AutoField(primary_key = True)
	group_name = models.CharField(max_length = 50, unique = True)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	def __str__(self):
		return self.group_name
	
	class Meta:
		db_table = "groups"

class group_permissions(models.Model):
	role = models.CharField(max_length = 15)
	
	def __str__(self):
		return self.role
	
	class Meta:
		db_table = "group_permissions"

class list_of_countries(models.Model):
	country_id = models.AutoField(primary_key = True)
	country_name = models.CharField(max_length = 50)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	def __str__(self):
		return self.country_name.encode('utf8')
	
	class Meta:
		db_table = "list_of_countries"


class list_of_countries_states(models.Model):
	campus_state_id = models.AutoField(primary_key = True)
	country_id = models.ForeignKey('list_of_countries', on_delete = models.CASCADE,)
	state = models.CharField(max_length = 50)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	def __str__(self):
		return self.state.encode('utf8')
	
	class Meta:
		db_table = "list_of_countries_states"

class list_of_titles(models.Model):
	title_id = models.AutoField(primary_key = True)
	title = models.CharField(max_length = 10)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	def __str__(self):
		return self.title
	
	class Meta:
		db_table = "list_of_titles"

class organisations(models.Model):
	organisations_id = models.AutoField(primary_key = True)
	organisation_name = models.CharField(max_length = 255)
	organisation_website = models.CharField(max_length = 50)
	organisation_email = models.CharField(max_length = 100)
	
	def __str__(self):
		return self.organisation_name
	
	class Meta:
		db_table = "organisations"

	
class organisations_campus(models.Model):
	organisations_id = models.ForeignKey('organisations', on_delete = models.CASCADE,)
	campus_nickname = models.CharField(max_length = 100)
	campus_phone = models.CharField(max_length = 11, null=True)
	campus_fax = models.CharField(max_length = 11, null=True)
	campus_address1 = models.CharField(max_length = 255, null=True)
	campus_address2 = models.CharField(max_length = 255, null=True)
	campus_address3 = models.CharField(max_length = 255, null=True)
	campus_suburb = models.CharField(max_length = 50)
	campus_state_id = models.ForeignKey('list_of_countries_states', on_delete = models.CASCADE,)
	campus_country_id = models.ForeignKey('list_of_countries', on_delete = models.CASCADE,)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	class Meta:
		db_table = "organisations_campus"



class project(models.Model):
	project_id = models.AutoField(primary_key = True)
	project_name = models.CharField(max_length = 255)
	project_description = models.TextField()
	organisations_id = models.ForeignKey('organisations', on_delete = models.CASCADE,)
	project_start_date = models.DateTimeField()
	project_end_date = models.DateTimeField()
	project_status = models.CharField(max_length = 15, choices = PROJECT_STATUS_CHOICE, default = 'New')
	
	def __str__(self):
		return self.project_name
	
	class Meta:
		db_table = "project"
	
	
class project_customers(models.Model):
	project_customers_id = models.AutoField(primary_key = True)
	project_id = models.ForeignKey('project', on_delete = models.CASCADE,)
	customer_id = models.ForeignKey('customers', on_delete = models.CASCADE,)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)
	
	class Meta:
		db_table = "project_customers"	
	

class project_groups(models.Model):
	project_id = models.ForeignKey('project', on_delete = models.CASCADE,)
	groups_id = models.ForeignKey('groups', on_delete = models.CASCADE,)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)
	
	class Meta:
		db_table = "project_groups"
		

class project_history(models.Model):
	project_history_id = models.AutoField(primary_key = True)
	project_id = models.ForeignKey('project', on_delete = models.CASCADE,)
	user_id = models.ForeignKey(User, on_delete = models.CASCADE, null = True)
	user_infomation = models.CharField(max_length = 255)
	project_history = models.TextField()
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)	
	
	class Meta:
		db_table = "project_history"

class project_stages(models.Model):
	project_stages_id = models.AutoField(primary_key = True)
	project_id = models.ForeignKey('project', on_delete = models.CASCADE,)
	stages_id = models.ForeignKey('stages', on_delete = models.CASCADE,)
	audit_date = models.DateTimeField(auto_now = True)
	
	class Meta:
		db_table = "project_stages"


class project_tasks(models.Model):
	project_tasks = models.AutoField(primary_key = True)
	project_id = models.ForeignKey('project', on_delete = models.CASCADE, db_column = 'project_id')
	task_id = models.ForeignKey('tasks', on_delete = models.CASCADE, db_column = 'task_id')
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)		
	
	class Meta:
		db_table = "project_tasks"


class stages(models.Model):
	stages_id = models.AutoField(primary_key = True)
	group_id = models.ForeignKey('groups', on_delete = models.CASCADE,)
	stage = models.CharField(max_length = 45)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	def __str__(self):
		return self.stage
	
	class Meta:
		db_table = "stages"
		

class tasks(models.Model):
	tasks_id = models.AutoField(primary_key = True)
	task_short_description = models.CharField(max_length = 255)
	task_long_description = models.TextField()
	organisations_id = models.ForeignKey('organisations', on_delete = models.CASCADE,)
	task_start_date = models.DateTimeField(auto_now = True) 
	task_end_date = models.DateTimeField()
	task_assigned_to = models.ForeignKey(User, null = True, blank = True)
	task_status = models.CharField(max_length = 15, choices = PROJECT_STATUS_CHOICE, default = 'New')
	
	def __str__(self):
		return self.task_short_description
	
	class Meta:
		db_table = "tasks"

class tasks_actions(models.Model):
	tasks_actions_id = models.AutoField(primary_key = True)
	tasks_id = models.ForeignKey('tasks', on_delete = models.CASCADE,)
	task_action = models.TextField()
	submitted_by = models.ForeignKey(User,)
	audit_date = models.DateTimeField(auto_now = True)		
	
	class Meta:
		db_table = "tasks_actions"	

class tasks_customers(models.Model):
	tasks_customers_id = models.AutoField(primary_key = True)
	customer_id = models.ForeignKey('customers', on_delete = models.CASCADE,)	
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)	
	
	class Meta:
		db_table = "tasks_customers"
		
class tasks_groups(models.Model):
	tasks_id = models.ForeignKey('tasks', on_delete = models.CASCADE,)
	groups_id = models.ForeignKey('groups', on_delete = models.CASCADE,)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)
	
	class Meta:
		db_table = "tasks_groups"
		
class tasks_history(models.Model):
	tasks_history_id = models.AutoField(primary_key = True)
	tasks_id = models.ForeignKey('tasks', on_delete = models.CASCADE,)
	user_id = models.ForeignKey(User, on_delete = models.CASCADE,)
	user_infomation = models.CharField(max_length = 255)	
	task_history = models.TextField()
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	audit_date = models.DateTimeField(auto_now = True)	
	
	class Meta:
		db_table = "tasks_history"
		

class user_groups(models.Model):
	username = models.ForeignKey(User,)
	group_id = models.ForeignKey('groups', on_delete = models.CASCADE,)
	user_group_permission = models.ForeignKey('group_permissions', on_delete = models.CASCADE,)
	is_deleted = models.CharField(max_length = 5, choices = IS_DELETED_CHOICE, default = 'FALSE')
	
	class Meta:
		db_table = "user_groups"	
		

	
