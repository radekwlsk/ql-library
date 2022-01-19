import strawberry.django

from strawberry.django import auto

from .. import models
from . import enums


@strawberry.django.input(models.Book)
class BookCreateInput:
    author_id: strawberry.ID
    category: enums.BookCategory
    language: enums.BookLanguage = enums.BookLanguage.EN
    pages: auto
    title: auto


@strawberry.django.input(models.Book, partial=True)
class BookUpdateInput:
    author_id: strawberry.ID
    category: enums.BookCategory
    language: enums.BookLanguage
    pages: auto
    title: auto
