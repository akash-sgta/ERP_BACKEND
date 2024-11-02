# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util._models.country import Country
# =====================================================================


class Iso(ChangeLog):

    class Meta:
        verbose_name_plural = "ISO"
        unique_together = ("country",)

    code = models.CharField(
        max_length=15,
        blank=False,
    )
    country = models.ForeignKey(
        Country,
        null=False,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        return super(Iso, self).save(*args, **kwargs)

    def __str__(self):
        return "{}{} {}".format(super(Iso, self).__str__(), self.code, self.country)
