# =====================================================================
from django.db import models
from django.utils import timezone
from django.db.utils import IntegrityError

from util._models._manager.change_log import ChangeLogModelManager
from util.functions import update_change_log, update_active_status, update_reference_objects


# =====================================================================


class ChangeLog(models.Model):

    class Meta:
        abstract = True
        unique_together = ()

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

    objects = ChangeLogModelManager()

    def save(self, del_flag=False, *args, **kwargs):
        C_DEL_FLAG = "del_flag"

        kwargs.update({C_DEL_FLAG: del_flag})
        update_change_log(_model=self, *args, **kwargs)
        _stat = update_active_status(_model=self, *args, **kwargs)
        kwargs.pop(C_DEL_FLAG)

        try:
            obj_ref = super(ChangeLog, self).save(*args, **kwargs)
        except IntegrityError:
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
                return super(ChangeLog, self).delete(*args, **kwargs)
        except KeyError:
            return self.save(del_flag=True)

    def __str__(self):
        return "[{}]".format("X" if self.is_active else "")
