# =====================================================================
from patient._serializers.patient import Patient as Serializer
from patient._models.patient import Patient as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Patient(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
