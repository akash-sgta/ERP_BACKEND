# =====================================================================
from staff._serializers.doctor import Doctor as Serializer
from staff._models.doctor import Doctor as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Doctor(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
