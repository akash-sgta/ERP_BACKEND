# =====================================================================
from django.db import models
from django.utils import timezone
from django.db.models import Manager

# =====================================================================


class ChangeLogQuerySet(models.QuerySet):

    def _filter(self, include_deleted=False, *args, **kwargs):
        if include_deleted:
            return self.filter(*args, **kwargs)
        else:
            return self.filter(is_active=True, *args, **kwargs)

    def _all(self, include_deleted=False, *args, **kwargs):
        return self._filter(include_deleted=include_deleted)

    def _get(self, include_deleted=False, *args, **kwargs):
        if include_deleted:
            return self.get(is_active=True, *args, **kwargs)
        else:
            return self.get(*args, **kwargs)


class ChangeLogModelManager(Manager):
    def get_queryset(self):
        return ChangeLogQuerySet(self.model, using=self._db)


class ChangeLog(models.Model):
    C_USER_ID = "USER_ID"
    C_DEFAULT = "DEFAULT"
    C_FORCED = "FORCED"

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
            user_id = kwargs[self.C_USER_ID]
        except KeyError:
            user_id = self.C_DEFAULT
        finally:
            user_id = user_id.upper()

        if self.pk is None:
            self.createdBy = user_id
        else:
            self.changedBy = user_id

        return super(ChangeLog, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        try:
            if kwargs[self.C_FORCED] is True:
                return super(ChangeLog, self).delete(*args, **kwargs)
        except KeyError:
            self.is_active = False
            self.save()
            return
