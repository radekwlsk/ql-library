from functools import partial

import graphene
import graphene_django


class OffsetPaginationInput(graphene.InputObjectType):
    offset = graphene.Field(graphene.Int, default_value=0)
    limit = graphene.Field(graphene.Int, default_value=-1)


class PaginationDjangoListField(graphene_django.DjangoListField):
    def __init__(self, type, *args, **kwargs):
        kwargs.setdefault("pagination", graphene.Argument(OffsetPaginationInput))

        super().__init__(type, *args, **kwargs)

    def list_resolver(self, resolver, default_manager, root, info, **kwargs):
        pagination = kwargs.pop("pagination", None)
        queryset = super().list_resolver(
            self._underlying_type, resolver, default_manager, root, info, **kwargs
        )
        if pagination is None:
            return queryset
        start = pagination.get("offset", 0)
        limit = pagination.get("limit", -1)
        if limit == -1:
            return queryset[start:]
        else:
            stop = start + limit
            return queryset[start:stop]

    def get_resolver(self, parent_resolver):
        return partial(self.list_resolver, parent_resolver, self.get_manager())
