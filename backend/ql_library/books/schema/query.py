import graphene

from .types import AuthorType, BookType
from ..models import Book, Author


class BooksQuery(object):
    author = graphene.Field(
        AuthorType,
        id=graphene.Int(required=True),
    )
    authors = graphene.List(
        AuthorType,
        country_name=graphene.String(required=False)
    )

    book = graphene.Field(
        BookType,
        id=graphene.Int(required=True),
    )
    books = graphene.List(
        BookType,
        category=graphene.String(required=False),
        language=graphene.String(required=False),
    )

    def resolve_author(self, info, id):
        return Author.objects.get(pk=id)

    def resolve_authors(self, info, country_name=None):
        if country_name:
            return Author.objects.filter(country__iexact=country_name)
        else:
            return Author.objects.all()

    def resolve_book(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_books(self, info, category=None, language=None):
        filters = {}
        if category:
            filters.update(category=category)
        if language:
            filters.update(language=category)
        return Book.objects.filter(
            **filters
        )

