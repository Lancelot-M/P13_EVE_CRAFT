from django.core.management.base import BaseCommand
from crafts.management.commands.commands import Industry


class Command(BaseCommand):
    def handle(self, *args, **options):
        maker = Industry()
        maker.start_industry()
