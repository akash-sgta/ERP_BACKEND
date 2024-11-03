# =====================================================================
from django.db import models
from util._models.continent import Continent
from util._models.master import Master

# =====================================================================


class Country(Master):
    class Meta:
        unique_together = Master.Meta.unique_together + (
            "continent",
            "name",
        )
        verbose_name_plural = "Countries"

    continent = models.ForeignKey(
        Continent,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=127,
        blank=False,
    )
    iso = models.CharField(
        max_length=17,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}".format(self.continent, super(Country, self).__str__(), self.name)
