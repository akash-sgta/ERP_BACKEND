# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog

# =====================================================================


class Continent(ChangeLog):

    class Meta:
        verbose_name_plural = "Continents"

    name = models.CharField(
        max_length=127,
        blank=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Continent, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)
