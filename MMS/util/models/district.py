# =====================================================================
from django.db import models
from util.models.state import State
from util.models.change_log import ChangeLog

# =====================================================================


class District(ChangeLog):
    class Meta:
        abstract = False
        unique_together = (
            "state",
            "name",
        )

    state = models.ForeignKey(
        State,
        on_delete=models.SET_NULL,
        null=True,
    )
    name = models.DateTimeField(blank=False)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(District, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}".format(self.state, self.name)
