import graphene

from ql_library.books.schema import BooksMutation, BooksQuery
from ql_library.users.schema import UsersQuery


class Query(graphene.ObjectType, UsersQuery, BooksQuery):
    # This class will inherit from multiple Queries as we begin to add more apps to our project.
    # See: https://docs.graphene-python.org/projects/django/en/latest/tutorial-plain/
    pass


class Mutation(graphene.ObjectType, BooksMutation):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
