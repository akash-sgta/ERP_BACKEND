# =====================================================================
from util._serializers.continent import Continent as Serializer
from util._models.continent import Continent as Model
from util._views.master import Master

# =====================================================================


class Continent(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
