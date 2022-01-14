import graphene

from ..models import (
    Author,
    Book,
)
from . import enums
from .types import BookType


class CreateBook(graphene.Mutation):
    class Arguments:
        author_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        language = graphene.Argument(
            enums.BookLanguage, required=False, default_value=enums.BookLanguage.EN.name
        )
        pages = graphene.Int(required=False)
        category = graphene.Argument(enums.BookCategory, required=False)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(
        cls, parent, info, author_id, title, language=None, pages=None, category=None
    ):
        author = Author.objects.get(id=author_id)
        book = Book.objects.create(
            author=author,
            title=title,
            language=language,
            pages=pages,
            category=category,
        )

        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        obj_id = graphene.ID(name="id")
        author_id = graphene.ID(required=False)
        title = graphene.String(required=False)
        language = graphene.Argument(enums.BookLanguage, required=False)
        pages = graphene.Int(required=False)
        category = graphene.Argument(enums.BookCategory, required=False)

    book = graphene.Field(BookType)

    @classmethod
    def mutate(cls, parent, info, obj_id, **kwargs):
        book = Book.objects.get(id=obj_id)
        if "author_id" in kwargs:
            book.author = Author.objects.get(pk=kwargs["author_id"])
        for field in ["title", "language", "pages", "category"]:
            if field in kwargs:
                setattr(book, field, kwargs[field])
        book.save()

        return UpdateBook(book=book)
