from django.contrib import admin

from ql_library.books import models
from ql_library.utils.admin import (
    linkify,
    linkify_set,
)


@admin.register(models.Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display_links = (
        "id",
        "__str__",
    )
    list_display = (
        "id",
        "__str__",
        "country",
        linkify_set("books"),
    )
    list_filter = ("country",)
    search_fields = ("name",)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related("books")


@admin.register(models.Book)
class BookAdmin(admin.ModelAdmin):
    list_display_links = (
        "id",
        "__str__",
    )
    list_display = (
        "id",
        "__str__",
        linkify("author"),
        "language",
        "category",
    )
    list_filter = (
        "language",
        "category",
    )
    list_select_related = ("author",)
    search_fields = (
        "title",
        "author__name",
    )
