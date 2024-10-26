# =====================================================================
from rest_framework.serializers import ModelSerializer
from util._models.change_log import ChangeLog as Model
from django.conf import settings

# =====================================================================


class ChangeLog(ModelSerializer):
    _hidden_fields = ("is_active",)
    _read_only_fields = (
        "id",
        "createdOn",
        "createdBy",
        "changedOn",
        "changedBy",
    )
    _to_upper_case = ("name",)

    def to_internal_value(self, data, *args, **kwargs):
        for field in self._to_upper_case:
            try:
                data[field] = data[field].upper()
            except KeyError:
                pass
        return super(ChangeLog, self).to_internal_value(data, *args, **kwargs)

    def is_valid(self, *args, **kwargs):
        is_valid = super(ChangeLog, self).is_valid(*args, **kwargs)
        if not is_valid:
            if not settings.DEBUG:
                _message_01 = "Contact Administrator : email@gmail.com"
            else:
                _message_01 = "Contact Administrator : Entry Exists"
            try:
                if (
                    type(self.errors["non_field_errors"]) != str
                    and self._errors["non_field_errors"][0].code == "unique"
                ):
                    self._errors["non_field_errors"] = _message_01
            except KeyError:
                pass
        return is_valid

    def to_representation(self, instance):
        return super(ChangeLog, self).to_representation(instance)
