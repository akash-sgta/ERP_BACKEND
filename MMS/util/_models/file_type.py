# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog

# =====================================================================


class FileType(ChangeLog):

    class Meta:
        verbose_name_plural = "File Types"
        unique_together = ("code",)

    code = models.CharField(
        max_length=7,
        blank=False,
    )
    name = models.CharField(
        max_length=127,
        blank=True,
    )

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        self.code = self.code.upper()
        return super(FileType, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.code)
