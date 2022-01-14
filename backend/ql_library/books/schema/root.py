import graphene

from ..models import (
    Author,
    Book,
)
from . import (
    mutations,
    types,
)


class BooksQuery(graphene.ObjectType):
    class Meta:
        abstract = True

    author = graphene.Field(
        types.AuthorType,
        obj_id=graphene.Argument(graphene.Int, required=True, name="id"),
    )
    authors = graphene.List(
        types.AuthorType, country_name=graphene.String(required=False)
    )

    book = graphene.Field(
        types.BookType,
        obj_id=graphene.Argument(graphene.Int, required=True, name="id"),
    )
    books = graphene.List(
        types.BookType,
        category=graphene.String(required=False),
        language=graphene.String(required=False),
    )

    @staticmethod
    def resolve_author(parent, info, obj_id):
        return Author.objects.get(id=obj_id)

    @staticmethod
    def resolve_authors(parent, info, country_name=None):
        if country_name:
            return Author.objects.filter(country__iexact=country_name)
        else:
            return Author.objects.all()

    @staticmethod
    def resolve_book(parent, info, obj_id):
        return Book.objects.get(id=obj_id)

    @staticmethod
    def resolve_books(parent, info, category=None, language=None):
        filters = {}
        if category:
            filters.update(category=category)
        if language:
            filters.update(language=category)
        return Book.objects.filter(**filters)


class BooksMutation(graphene.ObjectType):
    class Meta:
        abstract = True

    create_book = mutations.CreateBook.Field()
    update_book = mutations.UpdateBook.Field()
