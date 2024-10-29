# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import create_random, validate_string_len
from profile._models.profile import Profile

# =====================================================================


class Patient(ChangeLog):
    class Meta:
        verbose_name_plural = "Patients"

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        return super(Patient, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}".format(
            self.profile, super(Patient, self).__str__(), self.pid
        )
