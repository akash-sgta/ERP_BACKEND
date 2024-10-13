# =====================================================================
from django.db import models
from util.models.change_log import ChangeLog

# =====================================================================


class Continent(ChangeLog):
    class Meta:
        abstract = False

    name = models.DateTimeField(
        blank=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Continent, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)
