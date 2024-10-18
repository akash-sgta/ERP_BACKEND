# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import create_random, validate_string_len
from _user._models.profile import Profile

# =====================================================================


class Doctor(ChangeLog):
    class Meta:
        verbose_name_plural = "Doctors"

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
                    _pid = create_random(
                        stlen=15,
                        symbols=False,
                        lower_case=False,
                        numbers=True,
                        randomize=True,
                    )
                    Doctor.objects.get(pid=_pid)
                except Doctor.DoesNotExist:
                    break
            self.pid = _pid
        return super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}".format(self.profile, self.pid)