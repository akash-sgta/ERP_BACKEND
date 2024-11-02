# =====================================================================
from util._serializers.iso import Iso as Serializer
from util._models.iso import Iso as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Iso(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
