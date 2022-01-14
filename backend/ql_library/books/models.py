from django.db import models
from django.utils.translation import gettext_lazy as _

from . import choices


class Author(models.Model):
    name = models.CharField(_("Author name"), max_length=255)
    birthday = models.DateField(_("Birthday"), null=True, blank=True)
    country = models.CharField(
        _("Author's nationality"), max_length=255, null=True, blank=True
    )

    def __str__(self):
        return self.name


class Book(models.Model):
    author = models.ForeignKey(
        "books.Author", related_name="books", on_delete=models.CASCADE
    )
    title = models.CharField(max_length=255)
    language = models.CharField(
        max_length=2,
        choices=choices.BookLanguage.choices,
        default=choices.BookLanguage.EN,
    )
    pages = models.PositiveSmallIntegerField(null=True, blank=True)
    category = models.CharField(
        max_length=16, choices=choices.BookCategory.choices, null=True
    )

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ["author", "title", "language"]
