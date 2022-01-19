import graphene

from . import enums


class AuthorFilter(graphene.InputObjectType):
    id = graphene.ID()
    name = graphene.String()
    country = graphene.Field(graphene.String, name="countryName")


class BookFilter(graphene.InputObjectType):
    id = graphene.ID()
    author_id = graphene.ID()
    title = graphene.String()
    category = enums.BookCategory()
    language = enums.BookLanguage()


class BookCreateInput(graphene.InputObjectType):
    author_id = graphene.ID(required=True)
    title = graphene.String(required=True)
    category = enums.BookCategory()
    language = graphene.Field(enums.BookLanguage, default_value=enums.BookLanguage.EN)
    pages = graphene.Int()


class BookUpdateInput(graphene.InputObjectType):
    author_id = graphene.ID()
    title = graphene.String()
    category = enums.BookCategory()
    language = enums.BookLanguage()
    pages = graphene.Int()
