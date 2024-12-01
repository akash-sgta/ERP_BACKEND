# =====================================================================
from django.db import models, IntegrityError, transaction
from django.utils import timezone

from util._models._manager.company import CompanyModelManager as ModelManager
from util.functions import (
    update_change_log,
    update_active_status,
    update_reference_objects,
    cust_check_save,
)


# =====================================================================


class Company(models.Model):

    class Meta:
        verbose_name_plural = "Companies"
        unique_together = ("name",)

    name = models.CharField(
        max_length=127,
        blank=False,
    )

    createdOn = models.DateTimeField(
        blank=True,
        default=timezone.now,
    )
    createdBy = models.CharField(
        blank=True,
        max_length=127,
    )
    changedOn = models.DateTimeField(
        blank=True,
        auto_now=True,
    )
    changedBy = models.CharField(
        blank=True,
        max_length=127,
    )

    is_active = models.BooleanField(
        default=True,
    )

    objects = ModelManager()

    def check_save(self, *args, **kwargs):
        return cust_check_save(_model=self, *args, **kwargs)

    def save(self, del_flag=False, *args, **kwargs):
        C_DEL_FLAG = "del_flag"
        C_USER = "user"

        self.name = self.name.upper()

        kwargs.update({C_DEL_FLAG: del_flag, C_USER: self.changedBy})
        update_change_log(_model=self, *args, **kwargs)
        _stat = update_active_status(_model=self, *args, **kwargs)
        kwargs.pop(C_DEL_FLAG)
        kwargs.pop(C_USER)

        if self.check_save():
            if _stat[0] != _stat[1]:
                kwargs.update({C_DEL_FLAG: del_flag})
                update_reference_objects(_model=self, *args, **kwargs)
                kwargs.pop(C_DEL_FLAG)

        return super(Company, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        C_FORCED = "FORCED"

        try:
            if kwargs[C_FORCED]:
                kwargs.pop(C_FORCED)
                return super(Company, self).delete(*args, **kwargs)
        except KeyError:
            return self.save(del_flag=True)

    def __str__(self):
        return "[{}]{}".format("X" if self.is_active else "", self.name)
