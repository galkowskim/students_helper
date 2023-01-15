from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from base.models import CustomUser
from django.db import models


class Project(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class Task(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=200, null=False)
    content = models.TextField(null=True, blank=True)
    status_of_completion = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)

    class ProrityLevels(models.TextChoices):
        LOW = "C", _('Low')
        MEDIUM = "B", _("Medium")
        HIGH = 'A', _("High")

    priority_level = models.CharField(
        max_length=1,
        choices=ProrityLevels.choices,
        default=ProrityLevels.MEDIUM,
    )

    def __str__(self):
        return self.title

    class Meta:
        order_with_respect_to = 'priority_level'
