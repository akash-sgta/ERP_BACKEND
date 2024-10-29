# =====================================================================
from staff._serializers.nurse import Nurse as Serializer
from staff._models.nurse import Nurse as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Nurse(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
