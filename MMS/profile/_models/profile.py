# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util._models.government_id_type import GovernmentIdType
from util._models.file import File
from util.functions import validate_phone_number
from profile._models.address import Address
from django.contrib.auth.models import User

# =====================================================================


class Profile(ChangeLog):
    class Meta:
        verbose_name_plural = "Profiles"
        unique_together = (
            "user",
            "address",
        )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.OneToOneField(
        Address,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    government_id_type = models.ForeignKey(
        GovernmentIdType,
        on_delete=models.SET_NULL,
        null=True,
    )
    government_id_file = models.OneToOneField(
        File,
        on_delete=models.SET_NULL,
        null=True,
        related_name="government_id_file",
    )
    image_file = models.OneToOneField(
        File,
        on_delete=models.SET_NULL,
        null=True,
        related_name="image_file",
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

    email = models.EmailField(
        blank=True,
    )
    phone_office = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number],
    )
    phone_home = models.CharField(
        max_length=15,
        blank=True,
        validators=[validate_phone_number],
    )

    government_id = models.CharField(
        max_length=127,
        unique=True,
    )

    def save(self, *args, **kwargs):
        self.first_name = self.first_name.upper()
        self.middle_name = self.middle_name.upper()
        self.last_name = self.last_name.upper()
        self.government_id = self.government_id.upper()
        return super(Profile, self).save(*args, **kwargs)

    def __str__(self):
        return "{}->{}{}_{}".format(
            self.user,
            super(Profile, self).__str__(),
            self.first_name,
            self.last_name,
        )
