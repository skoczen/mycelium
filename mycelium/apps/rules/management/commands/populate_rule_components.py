from rules.tasks import populate_rule_components
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = "Repopulate the rule components."
    __test__ = False

    def handle(self, *args, **options):
        populate_rule_components()