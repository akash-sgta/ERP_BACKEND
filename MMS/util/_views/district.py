# =====================================================================
from util._serializers.district import District as Serializer
from util._models.district import District as Model
from util._views.master import Master

# =====================================================================


class District(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
