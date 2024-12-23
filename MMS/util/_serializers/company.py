# =====================================================================
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ErrorDetail
from rest_framework.serializers import ModelSerializer
from django.conf import settings
from util._models.company import Company as Model
from util.functions import Custom


# =====================================================================
custom_ref = Custom()


class Company(ModelSerializer):

    class Meta:
        model = Model
        hidden_fields = (
            "is_active",
            "company",
        )
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
        )

    def to_internal_value(self, data):
        custom_ref.cust_to_internal_value(model_ref=self, data=data)
        return super(Company, self).to_internal_value(data)

    def is_valid(self, *args, **kwargs):
        is_valid = super(Company, self).is_valid(*args, **kwargs)
        return custom_ref.cust_is_valid(
            model_ref=self, is_valid=is_valid, *args, **kwargs
        )
