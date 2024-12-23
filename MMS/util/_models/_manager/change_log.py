# =====================================================================
from django.db.models import Manager


# =====================================================================


class ChangeLogModelManager(Manager):

    def _filter(self, include_deleted=False, *args, **kwargs):
        if include_deleted:
            ref = self.filter(*args, **kwargs)
        else:
            ref = self.filter(is_active=True, *args, **kwargs)
        return ref

    def all_(self, include_deleted=False, *args, **kwargs):
        return self.filter_(include_deleted=include_deleted)

    def _get(self, include_deleted=False, *args, **kwargs):
        if include_deleted:
            ref = self.get(is_active=True, *args, **kwargs)
        else:
            ref = self.get(*args, **kwargs)
        return ref
