# =====================================================================
from django.utils import timezone
from django.db import models
from util._models.change_log import ChangeLog
from _user._models.profile import Profile

# =====================================================================


class Patient(ChangeLog):
    class Meta:
        verbose_name_plural = "Patients"

    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )

    def save(self, *args, **kwargs):
        return super(Patient, self).save(*args, **kwargs)
