# =====================================================================
from django.db import models, IntegrityError, transaction
from django.utils import timezone

from util._models._manager.company import CompanyModelManager as ModelManager
from util.functions import Custom


# =====================================================================
custom_ref = Custom()


class Company(models.Model):
    """
    Model representing a company.
    """

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
        return custom_ref.cust_check_save(model_ref=self, *args, **kwargs)

    def save(self, del_flag=False, *args, **kwargs):
        self.name = self.name.upper()

        kwargs.update({custom_ref.DEL_FLAG: del_flag})
        kwargs.update({custom_ref.USER: f"{self.changedBy}".upper()})
        custom_ref.update_change_log(model_ref=self, *args, **kwargs)
        _stat = custom_ref.update_active_status(
            model_ref=self, *args, **kwargs
        )
        kwargs.pop(custom_ref.DEL_FLAG)
        kwargs.pop(custom_ref.USER)

        if self.check_save():
            if _stat[0] != _stat[1]:
                kwargs.update({custom_ref.DEL_FLAG: del_flag})
                custom_ref.update_reference_objects(
                    model_ref=self, *args, **kwargs
                )
                kwargs.pop(custom_ref.DEL_FLAG)

        return super(Company, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            if kwargs[custom_ref.FORCED]:
                kwargs.pop(custom_ref.FORCED, None)
        except KeyError:
            return self.save(del_flag=True)

        return super(Company, self).delete(*args, **kwargs)

    def __str__(self):
        return "[{}]{}".format("X" if self.is_active else "", self.name)
