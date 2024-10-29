# =====================================================================
from util._serializers.change_log import ChangeLog as Serializer
from staff._models.doctor import Doctor as Model

# =====================================================================


class Doctor(Serializer):
    class Meta:
        model = Model
        _hidden_fields = Serializer._hidden_fields + ()
        fields = list()
        for field in model._meta.fields:
            if field.name not in _hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer._read_only_fields + ()
