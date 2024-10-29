# =====================================================================
from staff._serializers.doctor_heirarchy import DoctorHierarchy as Serializer
from staff._models.doctor_heirarchy import DoctorHierarchy as Model
from util._views.change_log import ChangeLog

# =====================================================================


class DoctorHierarchy(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model