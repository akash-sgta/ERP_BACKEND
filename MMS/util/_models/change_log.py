# =====================================================================
from django.db import models
from django.utils import timezone
from django.db.models import Manager

# =====================================================================


class ChangeLogQuerySet(models.QuerySet):

    def _filter(self, *args, **kwargs):
        try:
            is_active = not kwargs["is_deleted"]
        except KeyError:
            is_active = True
        return self.filter(is_active=is_active, *args, **kwargs)

    def _all(self, *args, **kwargs):
        try:
            is_active = not kwargs["is_deleted"]
        except KeyError:
            is_active = True
        return self.filter(is_active=is_active)

    def _get(self, *args, **kwargs):
        try:
            is_active = not kwargs["is_deleted"]
        except KeyError:
            is_active = True
        return self.get(is_active=is_active, *args, **kwargs)


class ChangeLogModelManager(Manager):
    def get_queryset(self):
        return ChangeLogQuerySet(self.model, using=self._db)


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

    objects = ChangeLogModelManager()

    def save(self, *args, **kwargs):

        try:
            user_id = kwargs["user_id"]
        except KeyError:
            user_id = "DEFAULT"
        finally:
            user_id = user_id.upper()

        if self.pk is None:
            self.createdBy = user_id
        else:
            self.changedBy = user_id

        return super(ChangeLog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            if kwargs["forced"] is True:
                return super(ChangeLog, self).delete(*args, **kwargs)
        except KeyError:
            self.is_active = False
            self.save()
            return
