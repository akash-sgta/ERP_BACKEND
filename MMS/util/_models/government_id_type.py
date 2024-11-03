# =====================================================================
from django.db import models
from util._models.master import Master

# =====================================================================


class GovernmentIdType(Master):

    class Meta:
        verbose_name_plural = "Government Id Types"
        unique_together = Master.Meta.unique_together + ("name",)

    name = models.CharField(
        max_length=127,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        return super(GovernmentIdType, self).save(*args, **kwargs)

    def __str__(self):
        return "{}{}".format(super(GovernmentIdType, self).__str__(), self.name)
