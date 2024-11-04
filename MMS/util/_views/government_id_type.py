# =====================================================================
from util._serializers.government_id_type import GovernmentIdType as Serializer
from util._models.government_id_type import GovernmentIdType as Model
from util._views.master import Master

# =====================================================================


class GovernmentIdType(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
