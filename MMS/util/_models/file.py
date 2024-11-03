# =====================================================================
from django.db import models
from util._models.master import Master
from util._models.file_type import FileType
from util.functions import validate_file_name

# =====================================================================


class File(Master):

    class Meta:
        verbose_name_plural = "Files"
        unique_together = Master.Meta.unique_together + ("name",)

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
        return "{}{}".format(super(File, self).__str__(), self.name)
