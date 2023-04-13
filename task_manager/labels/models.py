from django.db import models
from django.utils.translation import gettext_lazy as _


class Label(models.Model):
    name = models.CharField(max_length=100, unique=True, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('Label')
        verbose_name_plural = _('Labels')
