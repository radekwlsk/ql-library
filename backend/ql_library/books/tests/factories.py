import random

import factory

from ..models import Author, Book


class AuthorFactory(factory.DjangoModelFactory):
    name = factory.Faker("name")
    birthday = factory.Faker("date_of_birth", minimum_age=18, maximum_age=89)
    country = factory.Faker("country")

    class Meta:
        model = Author


class BookFactory(factory.DjangoModelFactory):
    author = factory.SubFactory(AuthorFactory)
    title = factory.Faker("sentence", nb_words=5, variable_nb_words=True)
    language = factory.Iterator(map(lambda ch: ch[0], Book.LANGUAGE_CHOICES))
    pages = factory.LazyFunction(lambda: random.randint(60, 1000))
    category = factory.Iterator(map(lambda ch: ch[0], Book.CATEGORY_CHOICES))

    class Meta:
        model = Book
