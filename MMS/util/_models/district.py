# =====================================================================
from django.db import models
from util._models.state import State
from util._models.master import Master

# =====================================================================


class District(Master):
    class Meta:
        unique_together = Master.Meta.unique_together + (
            "state",
            "name",
        )
        verbose_name_plural = "Districts"

    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
    )
    name = models.CharField(
        max_length=127,
        blank=False,
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(District, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}".format(self.state, super(District, self).__str__(), self.name)
