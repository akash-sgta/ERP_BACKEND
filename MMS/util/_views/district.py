# =====================================================================
from util._serializers.district import District as Serializer
from util._models.district import District as Model
from util._views.change_log import ChangeLog

# =====================================================================


class District(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
