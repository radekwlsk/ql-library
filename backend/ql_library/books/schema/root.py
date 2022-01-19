import graphene

from ..models import (
    Author,
    Book,
)
from . import (
    inputs,
    mutations,
    types,
)


class BooksQuery(graphene.ObjectType):
    class Meta:
        abstract = True

    author = graphene.Field(
        types.AuthorType,
        obj_id=graphene.Argument(graphene.ID, required=True, name="id"),
    )
    authors = graphene.List(
        graphene.NonNull(types.AuthorType),
        filters=inputs.AuthorFilter(required=False),
    )

    book = graphene.Field(
        types.BookType,
        obj_id=graphene.Argument(graphene.ID, required=True, name="id"),
    )
    books = graphene.List(
        graphene.NonNull(types.BookType),
        filters=inputs.BookFilter(required=False),
    )

    @staticmethod
    def resolve_author(parent, info, obj_id):
        return types.AuthorType.get_node(info, obj_id)

    @staticmethod
    def resolve_authors(parent, info, filters=None):
        qs = types.AuthorType.get_queryset(Author.objects.all(), info)
        if filters:
            qs = qs.filter(**filters)
        return qs

    @staticmethod
    def resolve_book(parent, info, obj_id):
        return types.BookType.get_node(info, obj_id)

    @staticmethod
    def resolve_books(parent, info, filters=None):
        qs = types.BookType.get_queryset(Book.objects.all(), info)
        if filters:
            qs = qs.filter(**filters)
        return qs


class BooksMutation(graphene.ObjectType):
    class Meta:
        abstract = True

    create_book = mutations.CreateBook.Field()
    update_books = mutations.UpdateBooks.Field()
