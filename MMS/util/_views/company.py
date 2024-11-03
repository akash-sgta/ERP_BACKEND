# =====================================================================
from util._serializers.company import Company as Serializer
from util._models.company import Company as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Company(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
