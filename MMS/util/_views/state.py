# =====================================================================
from util._serializers.state import State as Serializer
from util._models.state import State as Model
from util._views.master import Master

# =====================================================================


class State(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
