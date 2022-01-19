import graphene

from ql_library.books.schema.root import (
    BooksMutation,
    BooksQuery,
)
from ql_library.users.schema.root import UsersQuery


class Query(UsersQuery, BooksQuery, graphene.ObjectType):
    # This class will inherit from multiple Queries as we begin to add more apps to our project.
    # See: https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/
    pass


class Mutation(BooksMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
