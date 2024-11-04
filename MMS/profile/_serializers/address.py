# =====================================================================
from util._serializers.master import Master as Serializer
from profile._models.address import Address as Model

# =====================================================================


class Address(Serializer):
    class Meta:
        model = Model
        _hidden_fields = Serializer.Meta.hidden_fields + ()
        fields = list()
        for field in model._meta.fields:
            if field.name not in _hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer.Meta.read_only_fields + ()
