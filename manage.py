import os
from django.core import management

os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
if __name__ == "__main__":
    management.execute_from_command_line()
