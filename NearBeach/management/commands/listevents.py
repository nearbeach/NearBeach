from django.core.management.base import BaseCommand
from NearBeach import event_hooks

# Import runschedular so that we get its events
from . import runscheduler as _

class Command(BaseCommand):
    help = "Lists registered event which can be hooked onto"

    def add_arguments(self, parser):
        parser.add_argument("--prefix", action='append', type=str)

    @staticmethod
    def _has_prefix(event_name, prefixes):
        return any(
            event_name.startswith(p)
            for p in prefixes
        )

    def handle(self, *args, **options):
        print("options:", options)

        prefixes = options.get("prefix")
        prefix_msg_modifier=""
        if prefixes is None:
            prefixes = [""]
        else:
            prefix_msg_modifier = f"have the following prefixes [{', '.join(prefixes)}] " # Note needs trailing space


        found = []
        for e in sorted(event_hooks.list_event_types(), key=lambda e: e.name):
            if self._has_prefix(e.name, prefixes):
                found.append(f"- {e.name} ({", ".join(str(x) for x in e.types)})")

        if len(found) == 0:
            if prefix_msg_modifier == "":
                print("No events found")
            else:
                print(f"No events that {prefix_msg_modifier}found")
        else:
            print(f"These are the events currently registered for event which {prefix_msg_modifier}can be hooked onto:")
            print("key: event_name (arg types)")
            for line in found:
                print(line)
