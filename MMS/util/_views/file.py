# =====================================================================
from util._serializers.file import File as Serializer
from util._models.file import File as Model
from util._views.master import Master

# =====================================================================


class File(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
