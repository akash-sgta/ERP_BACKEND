# =====================================================================
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ModelSerializer
from django.conf import settings
from util._models.company import Company as Model
from util.functions import cust_to_internal_value, cust_is_valid


# =====================================================================


class Company(ModelSerializer):

    class Meta:
        model = Model
        _hidden_fields = ("is_active",)
        fields = list()
        for field in model._meta.fields:
            if field.name not in _hidden_fields:
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
        return super(Company, self).to_internal_value(data)

    def is_valid(self, *args, **kwargs):
        return cust_is_valid(_model=self, *args, **kwargs)
