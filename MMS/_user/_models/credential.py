# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util.functions import sha

# =====================================================================


class Credential(ChangeLog):

    class Meta:
        abstract = False

    user_name = models.CharField(
        max_length=127,
        blank=False,
    )
    password = models.CharField(
        max_length=255,
        blank=False,
    )

    def save(self, *args, **kwargs):
        self.user_name = self.user_name.upper()
        if self.password[:5] != "hash_":
            self.password = "hash_" + sha(self.password)
        return super(Credential, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.user_name)
