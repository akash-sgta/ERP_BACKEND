# =====================================================================
from util._serializers.master import Master as Serializer
from util._models.country import Country as Model

# =====================================================================


class Country(Serializer):

    class Meta:
        model = Model
        hidden_fields = Serializer.Meta.hidden_fields + ()
        fields = list()
        for field in model._meta.fields:
            if field.name not in hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer.Meta.read_only_fields + ()
