import strawberry.django

from strawberry.extensions import QueryDepthLimiter
from strawberry.tools import merge_types

from ql_library.books.schema.mutation import BooksMutation
from ql_library.books.schema.query import BooksQuery
from ql_library.users.schema.query import UsersQuery

types = []

Query = merge_types("Query", (BooksQuery, UsersQuery))
Mutation = merge_types("Mutation", (BooksMutation,))

schema = strawberry.Schema(
    Query,
    mutation=Mutation,
    types=types,
    extensions=[
        QueryDepthLimiter(max_depth=3),
    ],
)
