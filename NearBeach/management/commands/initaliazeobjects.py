from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from NearBeach.utils.admin import initalize_base_values


User = get_user_model()

class Command(BaseCommand):
    help = "Run this command will setup the base values"

    def handle(self, *args, **kwargs):
        admin_user = User.objects.get(is_admin=True).first()
        initalize_base_values(admin_user)
