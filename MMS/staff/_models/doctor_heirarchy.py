# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import create_random, validate_string_len
from staff._models.doctor import Doctor

# =====================================================================


class DoctorHierarchy(ChangeLog):
    class Meta:
        verbose_name_plural = "Doctor Hierarchy"
        unique_together = (
            "supervisor",
            "subordinate",
        )

    supervisor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="supervisor",
    )

    subordinate = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="subordinate",
    )

    def save(self, *args, **kwargs):
        return super(DoctorHierarchy, self).save(*args, **kwargs)

    def __str__(self):
        return "{}{}=>{}".format(
            super(DoctorHierarchy, self).__str__(),
            self.superviser,
            self.subordinate,
        )
