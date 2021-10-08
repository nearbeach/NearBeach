"""
This management file is designed for automatic testing purposes. It will not be
used in;
- production
- pypi

This function will only be used in;
- Automatic testing using CircleCI

This file can also be used - but currently not setup for;
- Automatic testing using travis
"""
import os
from django.core import management

os.environ['DJANGO_SETTINGS_MODULE'] = 'local.settings'
if __name__ == "__main__":
    management.execute_from_command_line()
