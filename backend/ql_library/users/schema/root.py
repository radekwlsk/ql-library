from django.contrib.auth import get_user_model

import graphene

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
    users = graphene.List(
        graphene.NonNull(types.UserType),
        filters=inputs.UserFilter(required=False),
    )

    def resolve_user(self, info, obj_id, **kwargs):
        return types.UserType.get_node(info, obj_id)

    def resolve_users(self, info, filters=None, **kwargs):
        qs = types.UserType.get_queryset(User.objects.all(), info)
        if filters:
            qs = qs.filter(**filters)
        return qs
