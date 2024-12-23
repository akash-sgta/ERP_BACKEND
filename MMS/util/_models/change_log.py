# =====================================================================
from django.db import models, transaction
from django.utils import timezone
from django.db.utils import IntegrityError

from util._models._manager.change_log import (
    ChangeLogModelManager as ModelManager,
)
from util.functions import Custom


# =====================================================================
custom_ref = Custom()


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

    objects = ModelManager()

    def check_save(self, *args, **kwargs):
        return custom_ref.cust_check_save(model_ref=self, *args, **kwargs)

    def save(self, del_flag=False, *args, **kwargs):
        kwargs.update(
            {
                custom_ref.DEL_FLAG: del_flag,
                custom_ref.USER: f"{self.changedBy}".upper(),
            }
        )
        custom_ref.update_change_log(model_ref=self, *args, **kwargs)
        _stat = custom_ref.update_active_status(
            model_ref=self, *args, **kwargs
        )
        kwargs.pop(custom_ref.DEL_FLAG)
        kwargs.pop(custom_ref.USER)

        _check_save = self.check_save()
        if _check_save[0]:
            if _stat[0] != _stat[1]:
                kwargs.update({custom_ref.DEL_FLAG: del_flag})
                custom_ref.update_reference_objects(
                    model_ref=self, *args, **kwargs
                )
                kwargs.pop(custom_ref.DEL_FLAG)
        else:
            pass

        return super(ChangeLog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            if kwargs[custom_ref.FORCED]:
                kwargs.pop(custom_ref.FORCED)
                return super(ChangeLog, self).delete(*args, **kwargs)
        except KeyError:
            return self.save(del_flag=True)

    def __str__(self):
        return "[{}]".format("X" if self.is_active else "")
