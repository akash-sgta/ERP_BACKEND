# =====================================================================
from staff._serializers.doctor import Doctor as Serializer
from staff._models.doctor import Doctor as Model
from util._views.master import Master

# =====================================================================


class Doctor(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
