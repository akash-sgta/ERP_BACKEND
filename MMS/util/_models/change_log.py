# =====================================================================
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils import timezone
from django.db.models import Manager
from django.db.utils import IntegrityError

# =====================================================================


class ChangeLogModelManager(Manager):

    def _filter(self, include_deleted=False, *args, **kwargs):
        if include_deleted:
            ref = self.filter(*args, **kwargs)
        else:
            ref = self.filter(is_active=True, *args, **kwargs)
        return ref

    def _all(self, include_deleted=False, *args, **kwargs):
        return self._filter(include_deleted=include_deleted)

    def _get(self, include_deleted=False, *args, **kwargs):
        if include_deleted:
            ref = self.get(is_active=True, *args, **kwargs)
        else:
            ref = self.get(*args, **kwargs)
        return ref


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

    def save(self, del_flag=False, *args, **kwargs):
        if del_flag:
            self.is_active = False
        else:
            self.is_active = True

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

        try:
            ref = super(ChangeLog, self).save(*args, **kwargs)
        except IntegrityError as e:
            ref = None
            if self.pk is not None:
                raise e
            else:
                unique_together = self._meta.unique_together
                if len(unique_together) > 0:
                    expression = "self.__class__.objects.get("
                    for unique_stack in unique_together:
                        for unique in unique_stack:
                            expression = "{}{}=self.{},".format(expression, unique, unique)
                    expression = "{})".format(expression[:-1])
                    try:
                        ref = eval(expression)
                    except ObjectDoesNotExist:
                        raise Exception("Foreign Key")
                    else:
                        if ref.is_active:
                            raise e
                        else:
                            ref.is_active = True
                            try:
                                ref = ref.save()
                            except Exception:
                                raise e
        return ref

    def delete(self, *args, **kwargs):
        try:
            if kwargs[self.C_FORCED] is True:
                return super(ChangeLog, self).delete(*args, **kwargs)
        except KeyError:
            self.save(del_flag=True)
            return
