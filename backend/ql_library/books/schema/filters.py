import strawberry.django

from .. import models
from . import enums


@strawberry.django.filters.filter(models.Book)
class BookFilter:
    language: enums.BookLanguage
    category: enums.BookCategory


@strawberry.django.filters.filter(models.Author)
class AuthorFilter:
    country: str = strawberry.django.field(name="countryName")
