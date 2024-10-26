# =====================================================================
from django.db import models
from util._models.change_log import ChangeLog
from util._models.file_type import FileType
from util.functions import validate_file_name

# =====================================================================


class File(ChangeLog):

    class Meta:
        verbose_name_plural = "Files"

    type = models.ForeignKey(
        FileType,
        on_delete=models.CASCADE,
        blank=True,
    )

    name = models.CharField(
        max_length=255,
        blank=False,
    )
    path = models.TextField()

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        if self.pk is None:
            self.name, self.type = validate_file_name(file_name=self.name)
        return super(File, self).save(*args, **kwargs)

    def __str__(self):
        return "{}".format(self.name)
