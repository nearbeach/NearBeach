from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(costs)
admin.site.register(customers)
admin.site.register(customers_campus)
admin.site.register(group_permissions)
admin.site.register(groups)
admin.site.register(list_of_countries_regions)
admin.site.register(list_of_countries)
admin.site.register(list_of_titles)
admin.site.register(organisations_campus)
admin.site.register(organisations)
admin.site.register(project_customers)
admin.site.register(project_groups)
admin.site.register(project_history)
admin.site.register(project_stages)
admin.site.register(project_tasks)
admin.site.register(project)
admin.site.register(stages)
admin.site.register(tasks_actions)
admin.site.register(tasks_customers)
admin.site.register(tasks_groups)
admin.site.register(tasks_history)
admin.site.register(tasks)
admin.site.register(user_groups)

