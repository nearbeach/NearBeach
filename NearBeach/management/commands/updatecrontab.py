from django.core.management.base import BaseCommand
from django.conf import settings


LINE_COMMAND = "python3 /oceansuite/manage.py runscheduler 2>&1\n"
LINE_TEMPLATE = "{timestr} {cmd}"
DEFAULT_TIME_STRING = "0 0 * * *"

class Command(BaseCommand):
    help = "Replaces the crontab entry for nearbeach"

    def handle(self, *args, **kwargs):
        with open("/etc/crontabs/nearbeach", "r+") as crontab:
            lines = crontab.readlines()

            found_index = -1
            for n, line in enumerate(lines):
                if line.endswith(LINE_COMMAND):
                    found_index = n
                    break

            write_line = LINE_TEMPLATE.format(
                timestr=getattr(settings, "CRONTAB_TIMESTR", DEFAULT_TIME_STRING),
                cmd=LINE_COMMAND,
            )

            if found_index == -1:
                lines.append(write_line)
            else:
                lines[found_index] = write_line

            crontab.seek(0)
            crontab.writelines(lines)
