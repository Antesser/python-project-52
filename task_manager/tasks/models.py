from django.db import models
from django.utils.translation import gettext_lazy as _

from task_manager.labels.models import Label
from task_manager.statuses.models import Status
from task_manager.users.models import User


class Task(models.Model):
    name = models.CharField(max_length=150, unique=True, blank=False)
    description = models.TextField(blank=True)
    author = models.ForeignKey(
        User,
        related_name="author",
        on_delete=models.PROTECT)
    executor = models.ForeignKey(
        User,
        related_name="executor",
        null=True,
        on_delete=models.PROTECT
    )
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    labels = models.ManyToManyField(
        Label,
        through="TaskLabelRelation",
        blank=True
    )
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['id']
        verbose_name = _('Task')
        verbose_name_plural = _('Tasks')


class TaskLabelRelation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    label = models.ForeignKey(Label, on_delete=models.PROTECT)
