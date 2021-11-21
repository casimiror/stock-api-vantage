from django.db import models
from django.utils.translation import ugettext as _


class AuditableModel(models.Model):
    """
    AuditableModel inherits from models.Model and implements the following
    fields for audit purposes: 'created_at', 'created_by', 'updated_at', 'updated_by'
    """

    created_at = models.DateTimeField(
        verbose_name=_("created at"), auto_now_add=True, editable=False
    )

    updated_at = models.DateTimeField(
        verbose_name=_("updated at"), auto_now=True, null=True, editable=False
    )

    class Meta:
        abstract = True
