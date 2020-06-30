import graphene

from graphene import ObjectType
from graphene_django.types import DjangoObjectType

from ..models import Author, Book


class CountryType(ObjectType):
    name = graphene.String()


class BookType(DjangoObjectType):
    class Meta:
        model = Book


class AuthorType(DjangoObjectType):
    country = graphene.Field(CountryType)
    books = graphene.List(
        BookType,
        category=graphene.String(required=False),
        language=graphene.String(required=False),
    )

    class Meta:
        model = Author

    def resolve_country(self, info, **kwargs):
        return CountryType(name=self.country)

    def resolve_books(self, info, category=None, language=None):
        filters = {}
        if category:
            filters.update(category=category)
        if language:
            filters.update(language=language)
        return self.books.filter(**filters)
