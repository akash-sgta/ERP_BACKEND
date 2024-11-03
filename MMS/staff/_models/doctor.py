# =====================================================================
from django.db import models
from util._models.master import Master
from profile._models.profile import Profile

# =====================================================================


class Doctor(Master):
    class Meta:
        verbose_name_plural = "Doctors"
        unique_together = Master.Meta.unique_together + ("profile",)

    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
    )

    def save(self, *args, **kwargs):
        return super(Doctor, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}".format(self.profile, super(Doctor, self).__str__(), self.pk)
