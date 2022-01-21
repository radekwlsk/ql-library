from django.contrib.auth import get_user_model

import graphene

from ...utils.graphene import PaginationDjangoListField
from . import (
    inputs,
    types,
)

User = get_user_model()


class UsersQuery(object):
    user = graphene.Field(
        types.UserType,
        obj_id=graphene.Argument(graphene.ID, required=True, name="id"),
    )
    users = PaginationDjangoListField(
        types.UserType,
        filters=inputs.UserFilter(required=False),
    )

    @staticmethod
    def resolve_user(parent, info, obj_id, **kwargs):
        return types.UserType.get_node(info, obj_id)

    @staticmethod
    def resolve_users(parent, info, filters=None, **kwargs):
        qs = types.UserType.get_queryset(User.objects.all(), info)
        if filters:
            qs = qs.filter(**filters)
        return qs
