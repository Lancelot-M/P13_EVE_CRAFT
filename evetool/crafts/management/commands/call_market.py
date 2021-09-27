from django.core.management.base import BaseCommand
from crafts.management.commands.commands import CallMarket


class Command(BaseCommand):
    def handle(self, *args, **options):
        maker = CallMarket()
        maker.main()
