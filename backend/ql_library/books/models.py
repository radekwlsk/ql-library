import enum

from django.db import models
from django.utils.translation import ugettext_lazy as _


class Author(models.Model):
    name = models.CharField(_("Author name"), max_length=255)
    birthday = models.DateField(_("Birthday"), null=True, blank=True)
    country = models.CharField(_("Author's nationality"), max_length=32, null=True, blank=True)

    def __str__(self):
        return self.name


class BookLanguage(enum.Enum):
    EN = _("English")
    PL = _("Polish")
    FR = _("French")
    DE = _("German")


class BookCategory(enum.Enum):
    FANTASY = _("Fantasy")
    NOVEL = _("Novel")
    COOKBOOK = _("Cookbook")
    BIOGRAPHY = _("Biography")


class Book(models.Model):
    LANGUAGE_CHOICES = tuple((e.name, e.value) for e in BookLanguage)
    CATEGORY_CHOICES = ((None, "N/A"),) + tuple((e.name, e.value) for e in BookCategory)

    author = models.ForeignKey(
        'books.Author',
        related_name='books',
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=255)
    language = models.CharField(
        max_length=2,
        choices=LANGUAGE_CHOICES,
        default=BookLanguage.EN.name,
    )
    pages = models.PositiveSmallIntegerField(null=True, blank=True)
    category = models.CharField(
        max_length=16,
        choices=CATEGORY_CHOICES,
        null=True,
    )

    class Meta:
        unique_together = ['author', 'title', 'language']
