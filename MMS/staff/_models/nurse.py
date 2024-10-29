# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import create_random, validate_string_len
from profile._models.profile import Profile

# =====================================================================


class Nurse(ChangeLog):
    class Meta:
        verbose_name_plural = "Nurses"

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
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
                    Nurse.objects.get(pid=_pid)
                except Nurse.DoesNotExist:
                    break
            self.pid = _pid
        return super(Nurse, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}".format(
            self.profile, super(Nurse, self).__str__(), self.pid
        )
