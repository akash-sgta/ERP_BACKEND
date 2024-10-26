# =====================================================================
from util._serializers.continent import Continent as Serializer
from util._models.continent import Continent as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Continent(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
