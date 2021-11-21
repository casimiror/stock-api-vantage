
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.db import models

from stocker.models import AuditableModel


class Customer(AuditableModel, User):
    user_phone = models.CharField(_("User Phone"),max_length=40)

    class Meta:

        verbose_name = _("registered customer")
        verbose_name_plural = _("registered customers")

    def __str__(self):
        return self.username
