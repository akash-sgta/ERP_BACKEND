# =====================================================================
from django.db import models
from util._models.continent import Continent
from util._models.change_log import ChangeLog

# =====================================================================


class Country(ChangeLog):
    class Meta:
        unique_together = (
            "continent",
            "name",
        )
        verbose_name_plural = "Countries"

    continent = models.ForeignKey(
        Continent,
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.CharField(
        max_length=127,
        blank=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}".format(self.continent, self.name)
