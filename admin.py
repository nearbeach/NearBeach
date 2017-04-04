from django.contrib import admin

# Register your models here.
from .models import customers
from .models import customers_campus
from .models import group_permissions
from .models import groups
from .models import list_of_countries_regions
from .models import list_of_countries
from .models import list_of_titles
from .models import organisations_campus
from .models import organisations
from .models import project_customers
from .models import project_groups
from .models import project_history
from .models import project_stages
from .models import project_tasks
from .models import project
from .models import stages
from .models import tasks_actions
from .models import tasks_customers
from .models import tasks_groups
from .models import tasks_history
from .models import tasks
from .models import user_groups





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

