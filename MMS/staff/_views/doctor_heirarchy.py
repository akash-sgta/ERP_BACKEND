# =====================================================================
from staff._serializers.doctor_heirarchy import DoctorHierarchy as Serializer
from staff._models.doctor_heirarchy import DoctorHierarchy as Model
from util._views.master import Master

# =====================================================================


class DoctorHierarchy(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
