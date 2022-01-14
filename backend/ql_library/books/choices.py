from django.db.models import TextChoices
from django.utils.translation import gettext_lazy as _


class BookLanguage(TextChoices):
    EN = "EN", _("English")
    PL = "PL", _("Polish")
    FR = "FR", _("French")
    DE = "DE", _("German")


class BookCategory(TextChoices):
    FANTASY = "FANTASY", _("Fantasy")
    NOVEL = "NOVEL", _("Novel")
    COOKBOOK = "COOKBOOK", _("Cookbook")
    BIOGRAPHY = "BIOGRAPHY", _("Biography")

    __empty__ = _("N/A")
