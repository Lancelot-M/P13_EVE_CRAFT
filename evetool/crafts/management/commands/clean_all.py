from django.core.management.base import BaseCommand
from crafts.management.commands.commands import DeleteData

class Command(BaseCommand):
    def handle(self, *args, **options):
        maker = DeleteData()
        maker.clean_all()