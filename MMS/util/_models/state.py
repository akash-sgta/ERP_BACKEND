# =====================================================================
from django.db import models
from util._models.country import Country
from util._models.master import Master

# =====================================================================


class State(Master):
    class Meta:
        unique_together = Master.Meta.unique_together + (
            "country",
            "name",
        )
        verbose_name_plural = "States"

    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=127,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}".format(self.country, super(State, self).__str__(), self.name)
