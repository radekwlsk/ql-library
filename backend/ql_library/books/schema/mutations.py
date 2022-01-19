import graphene

from ..models import (
    Author,
    Book,
)
from . import inputs
from .types import BookType


class CreateBook(graphene.Mutation):
    class Arguments:
        data = inputs.BookCreateInput(required=True)

    Output = BookType

    @classmethod
    def mutate(cls, parent, info, data=None):
        author = Author.objects.get(id=data.pop("author_id"))
        book = Book.objects.create(
            author=author,
            **data,
        )

        return book


class UpdateBooks(graphene.Mutation):
    class Arguments:
        data = inputs.BookUpdateInput(required=True)
        filters = inputs.BookFilter()

    Output = graphene.List(graphene.NonNull(BookType))

    @classmethod
    def mutate(cls, parent, info, data=None, filters=None):
        qs = Book.objects.all()
        if filters:
            qs = qs.filter(**filters)
        qs.update(**data)

        return list(qs)
