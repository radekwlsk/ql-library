from typing import List

import strawberry.django

from . import types


@strawberry.type
class UsersQuery:
    user: types.UserType = strawberry.django.field()
    users: List[types.UserType] = strawberry.django.field(pagination=True)
