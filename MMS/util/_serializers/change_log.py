# =====================================================================
from rest_framework.serializers import ModelSerializer
from util._models.change_log import ChangeLog as Model
from util.functions import Custom


# =====================================================================
custom_ref = Custom()


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
        )

    def to_internal_value(self, data):
        data = custom_ref.cust_to_internal_value(model_ref=self, data=data)
        self._validated_data = super().to_internal_value(data)
        return super(ChangeLog, self).to_internal_value(data)

    def validate(self, attrs):
        for key, value in self.initial_data.items():
            attrs[key] = value
        return attrs

    def is_valid(self, *args, **kwargs):
        is_valid = super(ChangeLog, self).is_valid(*args, **kwargs)
        return custom_ref.cust_is_valid(
            model_ref=self, is_valid=is_valid, *args, **kwargs
        )

    def update(self, instance, validated_data):
        # for key, value in validated_data.items():
        #     setattr(instance, key, value)
        return super(ChangeLog, self).update(instance, validated_data)
