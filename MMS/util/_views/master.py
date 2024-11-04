# =====================================================================
from util._serializers.master import Master as Serializer
from util._models.master import Master as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Master(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
