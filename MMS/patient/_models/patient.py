# =====================================================================
from django.utils import timezone
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import create_random, validate_string_len
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

    pid = models.CharField(
        max_length=15,
        unique=True,
        null=True,
        blank=True,
        validators=[validate_string_len],
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            while True:
                try:
                    _pid = create_random(stlen=15, symbols=False, lower_case=False)
                    Patient.objects.get(pid=_pid)
                except Patient.DoesNotExist:
                    break
            self.pid = _pid
        return super(Patient, self).save(*args, **kwargs)
