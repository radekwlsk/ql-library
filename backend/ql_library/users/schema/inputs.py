import graphene


class UserFilter(graphene.InputObjectType):
    id = graphene.ID()
    username = graphene.String()
