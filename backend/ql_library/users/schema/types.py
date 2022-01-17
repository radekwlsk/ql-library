from django.contrib.auth import get_user_model

import strawberry.django

from strawberry.django import auto

from . import filters


@strawberry.django.type(get_user_model(), filters=filters.UserFilter)
class UserType:
    id: auto
    name: auto
    username: auto
    email: auto
    date_joined: auto
