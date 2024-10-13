# =====================================================================
from django.db import models
from django.utils import timezone

# =====================================================================


class ChangeLog(models.Model):
    class Meta:
        abstract = True

    createdOn = models.DateTimeField(
        blank=True,
    )
    createdBy = models.CharField(
        blank=True,
        max_length=127,
    )
    changedOn = models.DateTimeField(
        blank=True,
        default=timezone.now,
    )
    changedBy = models.CharField(
        blank=True,
        max_length=127,
    )

    def save(self, *args, **kwargs):

        try:
            user_id = kwargs["USER_ID"]
        except KeyError:
            user_id = "DEFAULT"
        finally:
            user_id = user_id.upper()

        if self.createdOn == "":
            self.createdOn = self.changedOn
            self.createdBy = user_id
            del self.changedOn
        else:
            self.changedByBy = user_id

        return super(ChangeLog, self).save(*args, **kwargs)
