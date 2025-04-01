from django.core.management.base import BaseCommand
from django.conf import settings
import string
import os

LINE_COMMAND = "python3 {manage_path} runscheduler 2>&1\n"
LINE_TEMPLATE = "{timestr} {cmd}"
DEFAULT_TIME_STRING = "0 0 * * *"
ALLOWED_CHARS = set(string.digits + "/*-, ")
DEFAULT_CRONTAB_PATH = "/etc/crontabs/nearbeach"


class ContabTime:

    _fields = (
        "minutes",
        "hours",
        "day_of_month",
        "month",
        "day_of_week",
    )

    _valid_ranges = (
        (0, 59),
        (0, 23),
        (1, 31),
        (1, 12),
        (0, 6),
    )

    def __init__(self, mins=None, hrs=None, dom=None, month=None, dow=None, *args):
        self._minutes = mins
        self._hours = hrs
        self._day_of_month = dom
        self._month = month
        self._day_of_week = dow
        self._extras = args

    @staticmethod
    def _get_value(x, max_value):
        if x == "*":
            # replace x with a valid value
            return max_value
        return int(x)

    def _get_values(self, x, min_value):
        return list(map(lambda y, m=min_value: self._get_value(y, m), x))

    def _check_list(self, v, min_value, max_value):
        for x in v.split(","):
            if x == "":
                continue
            if not self._check_value(x, min_value, max_value):
                return False
        return True

    def _check_steps(self, v, min_value, max_value):
        if "/" in v:
            num, dom = v.split("/")
            if not self._check_value_in_range(num, min_value, max_value):
                return False
            if not self._check_value_in_range(dom, min_value, max_value):
                return False
        return True

    def _check_range(self, v, min_value, max_value):
        start, end = v.split("-")
        if not self._check_value_in_range(start, min_value, max_value):
            return False

        if "/" in end:
            if not self._check_steps(end, min_value, max_value):
                return False
        elif not self._check_value_in_range(end, min_value, max_value):
            return False
        return True

    def _check_value_in_range(self, v, min_value, max_value):
        value = self._get_value(v, min_value)
        if value < min_value or value > max_value:
            return False
        return True

    def _check_value(self, v, min_value=0, max_value=59):
        try:
            if len(set(v).difference(ALLOWED_CHARS)) > 0:
                return False
            elif "," in v:
                if not self._check_list(v, min_value, max_value):
                    return False
            elif "-" in v:
                if not self._check_range(v, min_value, max_value):
                    False
            elif "/" in v:
                if not self._check_steps(v, min_value, max_value):
                    return False
            elif not self._check_value_in_range(v, min_value, max_value):
                return False
        except:
            return False

        return True

    def validate(self):
        if len(self._extras) != 0 or any(
            getattr(self, "_" + f) is None for f in self._fields
        ):
            raise ValueError("Invalid crontab")

        for f, r in zip(self._fields, self._valid_ranges):
            v = getattr(self, "_" + f)
            x = self._check_value(v, min_value=r[0], max_value=r[1])
            if not x:
                raise ValueError("Invalid crontab")

    @staticmethod
    def from_string(timestr):
        return ContabTime(*timestr.split(" "))

    def __str__(self):
        return " ".join(
            f
            for f in map(lambda x: getattr(self, "_" + x), self._fields)
            if f is not None
        )


class Command(BaseCommand):
    help = "Replaces the crontab entry for nearbeach"

    def handle(self, *args, **kwargs):
        base_dir = getattr(settings, "BASE_DIR")
        if base_dir is None:
            raise ValueError("BASE_DIR not set")
        line_command = LINE_COMMAND.format(
            manage_path=os.path.join(base_dir, "manage.py")
        )

        timestr = getattr(settings, "CRONTAB_TIMESTR", DEFAULT_TIME_STRING)
        tab = ContabTime.from_string(timestr)
        tab.validate()

        with open(
            getattr(settings, "CRONTAB_PATH", DEFAULT_CRONTAB_PATH), "r+"
        ) as crontab:
            lines = crontab.readlines()

            found_index = -1
            for n, line in enumerate(lines):
                if line.endswith(line_command):
                    found_index = n
                    break

            write_line = LINE_TEMPLATE.format(
                timestr=timestr,
                cmd=line_command,
            )

            if found_index == -1:
                lines.append(write_line)
            else:
                lines[found_index] = write_line

            crontab.seek(0)
            crontab.writelines(lines)
