import strawberry.django

from strawberry.django import (
    auto,
    filters,
)

from .. import models
from . import enums


@strawberry.django.filters.filter(models.Book)
class BookFilter:
    id: auto
    title: auto
    author_id: strawberry.ID
    language: enums.BookLanguage
    category: enums.BookCategory


@strawberry.django.filters.filter(models.Author)
class AuthorFilter:
    id: auto
    name: filters.FilterLookup[str]
    country: str = strawberry.django.field(name="countryName")
