import random

import factory

from factory.django import DjangoModelFactory
from factory.fuzzy import FuzzyChoice

from .. import choices
from ..models import (
    Author,
    Book,
)


class AuthorFactory(DjangoModelFactory):
    name = factory.Faker("name")
    birthday = factory.Faker("date_of_birth", minimum_age=18, maximum_age=89)
    country = factory.Faker("country")

    class Meta:
        model = Author

    class Params:
        with_books = factory.Trait(
            books=factory.RelatedFactoryList(
                "ql_library.books.tests.factories.BookFactory",
                factory_related_name="author",
                size=lambda: random.randint(5, 30),
            )
        )


class BookFactory(DjangoModelFactory):
    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    language = FuzzyChoice(choices.BookLanguage.values)
    pages = factory.LazyFunction(lambda: random.randint(60, 1000))
    category = FuzzyChoice(choices.BookCategory.values)

    class Meta:
        model = Book
