from typing import (
    List,
    Optional,
)

import strawberry.django

from strawberry.django import auto

from .. import models
from . import (
    enums,
    filters,
)


@strawberry.type
class CountryType:
    name: Optional[str]


@strawberry.django.type(models.Book, filters=filters.BookFilter)
class BookType:
    id: auto
    author: "AuthorType"
    title: auto
    pages: auto
    language: enums.BookLanguage
    category: enums.BookCategory


@strawberry.django.type(models.Author, filters=filters.AuthorFilter)
class AuthorType:
    id: auto
    name: auto
    birthday: auto
    country: CountryType
    books: List["BookType"] = strawberry.django.field(pagination=True)

    @strawberry.field
    def country(self) -> CountryType:
        return CountryType(name=self.country)
