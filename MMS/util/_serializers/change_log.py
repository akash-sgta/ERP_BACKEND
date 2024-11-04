# =====================================================================
from rest_framework.serializers import ModelSerializer
from util._models.change_log import ChangeLog as Model
from util.functions import cust_to_internal_value, cust_is_valid


# =====================================================================


class ChangeLog(ModelSerializer):
    class Meta:
        model = Model
        hidden_fields = ("is_active",)
        fields = list()
        for field in model._meta.fields:
            if field.name not in hidden_fields:
                fields.append(field.name)
        read_only_fields = (
            "id",
            "createdOn",
            "createdBy",
            "changedOn",
            "changedBy",
            "company",
        )

    def to_internal_value(self, data):
        cust_to_internal_value(_model=self, data=data)
        return super(ChangeLog, self).to_internal_value(data)

    def is_valid(self, *args, **kwargs):
        return cust_is_valid(_model=self, *args, **kwargs)
