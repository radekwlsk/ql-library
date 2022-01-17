import strawberry

from .. import choices

BookLanguage = strawberry.enum(choices.BookLanguage)
BookCategory = strawberry.enum(choices.BookCategory)
