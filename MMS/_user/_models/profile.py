# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from _user._models.credential import Credential
from _user._models.address import Address

# =====================================================================


class Profile(ChangeLog):

    credential = models.ForeignKey(
        Credential,
        on_delete=models.SET_NULL,
        null=True,
    )
    address = models.ForeignKey(
        Address,
        on_delete=models.SET_NULL,
        null=True,
    )

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

    date_of_birth = models.DateField()

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.middle_name = self.middle_name.upper()
        self.last_name = self.last_name.upper()
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{} {}".format(self.credential, self.first_name, self.last_name)
