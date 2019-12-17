import graphene

from .types import BookType

from ..models import Book, Author


class CreateBook(graphene.Mutation):
    class Arguments:
        author_id = graphene.ID(required=True)
        title = graphene.String(required=True)
        language = graphene.String(required=False)
        pages = graphene.Int(required=False)
        category = graphene.String(required=False)

    book = graphene.Field(BookType)

    def mutate(self, info, author_id, title, language=None, pages=None, category=None):
        book = Book.objects.create(
            author_id=author_id,
            title=title,
            language=language,
            pages=pages,
            category=category,
        )

        return CreateBook(book=book)


class UpdateBook(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        author_id = graphene.ID(required=False)
        title = graphene.String(required=False)
        language = graphene.String(required=False)
        pages = graphene.Int(required=False)
        category = graphene.String(required=False)

    book = graphene.Field(BookType)

    def mutate(self, info, id, **kwargs):
        book = Book.objects.get(pk=id)
        if 'author_id' in kwargs:
            book.author = Author.objects.get(pk=kwargs['author_id'])
        for field in ['title', 'language', 'pages', 'category']:
            if field in kwargs:
                setattr(book, field, kwargs[field])
        book.save()

        return UpdateBook(book=book)


class BooksMutation(object):
    create_book = CreateBook.Field()
    update_book = UpdateBook.Field()
