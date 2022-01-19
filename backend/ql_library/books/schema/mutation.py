from typing import List

import strawberry.django

from strawberry.django import mutations

from . import (
    filters,
    inputs,
    types,
)


@strawberry.type
class BooksMutation:
    create_book: types.BookType = mutations.create(inputs.BookCreateInput)
    update_books: List[types.BookType] = mutations.update(
        inputs.BookUpdateInput, filters=filters.BookFilter
    )
