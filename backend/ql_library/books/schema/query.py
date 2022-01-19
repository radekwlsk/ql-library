from typing import List

import strawberry.django

from . import types


@strawberry.type
class BooksQuery:
    author: types.AuthorType = strawberry.django.field()
    authors: List[types.AuthorType] = strawberry.django.field(pagination=True)
    book: types.BookType = strawberry.django.field()
    books: List[types.BookType] = strawberry.django.field(pagination=True)
