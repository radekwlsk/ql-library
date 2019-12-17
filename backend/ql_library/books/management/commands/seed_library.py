import random

from django.core.management.base import BaseCommand
from ql_library.books.tests.factories import AuthorFactory, BookFactory


class Command(BaseCommand):
    help = 'Command to seed database with random authors and books'

    def add_arguments(self, parser):
        parser.add_argument(
            '--authors',
            action='store',
            type=int,
            required=True,
            dest='authors_count',
            help='How many authors to create',
        )
        parser.add_argument(
            '--min-books',
            action='store',
            type=int,
            default=1,
            required=False,
            dest='min_books',
            help='Minimum number of books per author',
        )
        parser.add_argument(
            '--max-books',
            action='store',
            type=int,
            default=10,
            required=False,
            dest='max_books',
            help='Maximum number of books per author',
        )

    def handle(self, *args, **options):
        authors = AuthorFactory.create_batch(options['authors_count'])
        for author in authors:
            num_books = random.randint(options['min_books'], options['max_books'])
            BookFactory.create_batch(num_books, author=author)
