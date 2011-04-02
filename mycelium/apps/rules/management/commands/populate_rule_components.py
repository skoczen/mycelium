from rules.tasks import populate_rule_components

class Command(BaseCommand):
    help = "Repopulate the rule components."
    __test__ = False

    def handle(self, *args, **options):
        populate_rule_components()