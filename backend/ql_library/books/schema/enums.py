import graphene

from .. import choices

BookLanguage = graphene.Enum.from_enum(choices.BookLanguage)
BookCategory = graphene.Enum.from_enum(choices.BookCategory)
