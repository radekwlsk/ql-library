import graphene

from graphene import ObjectType
from graphene_django.types import DjangoObjectType

from ...utils.graphene import PaginationDjangoListField
from ..models import (
    Author,
    Book,
)
from . import enums


class CountryType(ObjectType):
    name = graphene.String()


class BookType(DjangoObjectType):
    language = graphene.Field(enums.BookLanguage, required=True)
    category = graphene.Field(enums.BookCategory)

    class Meta:
        model = Book


class AuthorType(DjangoObjectType):
    country = graphene.Field(CountryType)
    books = PaginationDjangoListField(
        BookType,
        category=graphene.Argument(enums.BookCategory, required=False),
        language=graphene.Argument(enums.BookLanguage, required=False),
    )

    class Meta:
        model = Author

    @staticmethod
    def resolve_country(instance, info, **kwargs):
        return CountryType(name=instance.country)

    @staticmethod
    def resolve_books(instance, info, category=None, language=None):
        filters = {}
        if category:
            filters.update(category=category)
        if language:
            filters.update(language=language)
        return instance.books.filter(**filters)
