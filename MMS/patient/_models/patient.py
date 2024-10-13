# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog

# =====================================================================


class Patient(ChangeLog):

    first_name = models.CharField(
        max_length=127,
        blank=False,
    )
    middle_name = models.CharField(
        max_length=127,
        blank=True,
    )
    last_name = models.CharField(
        max_length=127,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.middle_name = self.middle_name.upper()
        self.last_name = self.last_name.upper()
        return super(Patient, self).save(*args, **kwargs)
