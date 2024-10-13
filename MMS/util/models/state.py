# =====================================================================
from django.db import models
from util.models.country import Country
from util.models.change_log import ChangeLog

# =====================================================================


class State(ChangeLog):
    class Meta:
        abstract = False
        unique_together = (
            "country",
            "name",
        )

    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.DateTimeField(blank=False)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}".format(self.country, self.name)
