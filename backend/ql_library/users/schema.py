import graphene

from django.contrib.auth import get_user_model
from graphene_django.types import DjangoObjectType

User = get_user_model()


class UserType(DjangoObjectType):
    class Meta:
        model = User


class UsersQuery(object):
    get_user = graphene.Field(
        UserType,
        id=graphene.Int(required=False),
        username=graphene.String(required=False),
    )
    get_users = graphene.List(UserType)

    def resolve_get_user(self, info, **kwargs):
        id = kwargs.get('id')
        username = kwargs.get('username')

        if id is not None:
            return User.objects.get(pk=id)

        if username is not None:
            return User.objects.get(username=username)

        return None

    def resolve_get_users(self, info, **kwargs):
        return User.objects.all()
