# =====================================================================
from django.db import models

from util._models.company import Company
from util._models.change_log import ChangeLog

# =====================================================================


class Master(ChangeLog):

    class Meta:
        abstract = True
        unique_together = ChangeLog.Meta.unique_together + ("company",)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return "{}.{}".format(self.company, super(Master, self).__str__())
