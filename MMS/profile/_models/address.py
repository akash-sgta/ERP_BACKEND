# =====================================================================
from django.db import models
from util._models.master import Master
from util._models.district import District

# =====================================================================


class Address(Master):
    class Meta:
        verbose_name_plural = "Addresses"
        unique_together = Master.Meta.unique_together + ("id",)

    id = models.AutoField(
        primary_key=True,
    )

    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
    )

    line_01 = models.CharField(
        max_length=127,
        blank=False,
    )
    line_02 = models.CharField(
        max_length=127,
        blank=True,
    )
    line_03 = models.CharField(
        max_length=127,
        blank=True,
    )
    line_04 = models.CharField(
        max_length=127,
        blank=True,
    )

    post_office = models.CharField(
        max_length=127,
        blank=False,
    )
    postal_code = models.CharField(
        max_length=15,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.post_office = self.post_office.upper()
        return super(Address, self).save(*args, **kwargs)

    def __str__(self):
        return "{}{}".format(super(Address, self).__str__(), self.pk)
