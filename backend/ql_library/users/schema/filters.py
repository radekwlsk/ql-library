from django.contrib.auth import get_user_model

import strawberry.django

from strawberry.django import (
    filters,
)


@strawberry.django.filters.filter(get_user_model())
class UserFilter:
    username: filters.FilterLookup[str]
