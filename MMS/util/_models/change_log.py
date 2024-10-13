# =====================================================================
from django.db import models
from django.utils import timezone

# =====================================================================


class ChangeLog(models.Model):
    class Meta:
        abstract = True

    createdOn = models.DateTimeField(
        blank=True,
        default=timezone.now,
    )
    createdBy = models.CharField(
        blank=True,
        max_length=127,
    )
    changedOn = models.DateTimeField(
        blank=True,
        auto_now=True,
    )
    changedBy = models.CharField(
        blank=True,
        max_length=127,
    )

    is_active = models.BooleanField(
        default=True,
    )

    def save(self, *args, **kwargs):

        try:
            user_id = kwargs["USER_ID"]
        except KeyError:
            user_id = "DEFAULT"
        finally:
            user_id = user_id.upper()

        if self.pk is None:
            self.createdBy = user_id
        else:
            self.changedBy = user_id

        return super(ChangeLog, self).save(*args, **kwargs)
