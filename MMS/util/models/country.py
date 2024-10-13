# =====================================================================
from django.db import models
from util.models.continent import Continent
from util.models.change_log import ChangeLog

# =====================================================================


class Country(ChangeLog):
    class Meta:
        abstract = False
        unique_together = (
            "continent",
            "name",
        )

    continent = models.ForeignKey(
        Continent,
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.DateTimeField(blank=False)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(Country, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}".format(self.continent, self.name)
