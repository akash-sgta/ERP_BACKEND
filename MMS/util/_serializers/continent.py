# =====================================================================
from util._serializers.master import Master as Serializer
from util._models.continent import Continent as Model

# =====================================================================


class Continent(Serializer):
    class Meta:
        model = Model
        _hidden_fields = Serializer.Meta._hidden_fields + ()
        fields = list()
        for field in model._meta.fields:
            if field.name not in _hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer.Meta._read_only_fields + ()
