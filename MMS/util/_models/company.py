# =====================================================================
from django.db import models, IntegrityError
from django.utils import timezone

from util.functions import update_change_log, update_active_status, update_reference_objects


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

    def save(self, del_flag=False, *args, **kwargs):
        C_DEL_FLAG = "del_flag"

        self.name = self.name.upper()

        kwargs.update({C_DEL_FLAG: del_flag})
        update_change_log(_model=self, *args, **kwargs)
        _stat = update_active_status(_model=self, *args, **kwargs)
        kwargs.pop(C_DEL_FLAG)

        try:
            obj_ref = super(Company, self).save(*args, **kwargs)
        except IntegrityError as e:
            pass
        else:
            if _stat[0] != _stat[1]:
                kwargs.update({C_DEL_FLAG: del_flag})
                update_reference_objects(_model=self, *args, **kwargs)

        return None

    def delete(self, *args, **kwargs):
        C_FORCED = "FORCED"

        try:
            if kwargs[C_FORCED]:
                return super(Company, self).delete(*args, **kwargs)
        except KeyError:
            return self.save(del_flag=True)

    def __str__(self):
        return "[{}]{}".format("X" if self.is_active else "", self.name)
