# =====================================================================
from util._serializers.change_log import ChangeLog as Serializer
from util._models.file_type import FileType as Model

# =====================================================================


class FileType(Serializer):

    class Meta:
        model = Model
        hidden_fields = Serializer._hidden_fields + ()
        fields = list()
        for field in model._meta.fields:
            if field.name not in hidden_fields:
                fields.append(field.name)
        read_only_fields = Serializer._read_only_fields + ()
