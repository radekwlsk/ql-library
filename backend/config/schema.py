from typing import List

import strawberry.django

from ql_library.books.schema import types as books_types
from ql_library.users.schema import types as users_types

types = []


@strawberry.type
class Query:
    """The root queries entry point"""

    # books
    author: books_types.AuthorType = strawberry.django.field()
    authors: List[books_types.AuthorType] = strawberry.django.field(pagination=True)
    book: books_types.BookType = strawberry.django.field()
    books: List[books_types.BookType] = strawberry.django.field(pagination=True)

    # users
    user: users_types.UserType = strawberry.django.field()
    users: List[users_types.UserType] = strawberry.django.field(pagination=True)


schema = strawberry.Schema(Query, types=types)
