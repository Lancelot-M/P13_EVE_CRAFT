from django.core.management.base import BaseCommand
from crafts.management.commands.commands import CreateDb


class Command(BaseCommand):
    def handle(self, *args, **options):
        maker = CreateDb()
        maker.create_db()
