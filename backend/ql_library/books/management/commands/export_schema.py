from django.core.management import BaseCommand

from strawberry.printer import print_schema

from config.schema import schema


class Command(BaseCommand):
    help = "Export GraphQL Schema"

    def handle(self, *args, **options):
        print(print_schema(schema))
