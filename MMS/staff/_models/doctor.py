# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import create_random, validate_string_len
from profile._models.profile import Profile

# =====================================================================


class Doctor(ChangeLog):
    class Meta:
        verbose_name_plural = "Doctors"

    profile = models.OneToOneField(
        Profile,
        on_delete=models.SET_NULL,
        null=True,
    )

    def save(self, *args, **kwargs):
        return super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}".format(self.profile, self.pid)
