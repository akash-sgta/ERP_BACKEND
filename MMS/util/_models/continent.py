# =====================================================================
from django.db import models
from util._models.master import Master

# =====================================================================


class Continent(Master):

    class Meta:
        verbose_name_plural = "Continents"
        unique_together = Master.Meta.unique_together + ("name",)

    name = models.CharField(
        max_length=127,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Continent, self).save(*args, **kwargs)

    def __str__(self):
        return "{}{}".format(super(Continent, self).__str__(), self.name)
