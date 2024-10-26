# =====================================================================
from util._serializers.government_id_type import GovernmentIdType as Serializer
from util._models.government_id_type import GovernmentIdType as Model
from util._views.change_log import ChangeLog

# =====================================================================


class GovernmentIdType(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
