# =====================================================================
from util._serializers.change_log import ChangeLog as Serializer
from util._models.master import Master as Model

# =====================================================================


class Master(Serializer):
    class Meta:
        model = Model
        hidden_fields = Serializer.Meta.hidden_fields + ("company",)
        fields = list()
        for field in model._meta.fields:
            if field.name not in hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer.Meta.read_only_fields + ()
