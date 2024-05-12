from django.db import models
from django.utils.translation import gettext_lazy as _


class TimestampsMixin(models.Model):
    created_at = models.DateTimeField(_("Дата создания"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Дата обновления"), auto_now=True, editable=False)

    class Meta:
        abstract = True
