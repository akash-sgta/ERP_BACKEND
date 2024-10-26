# =====================================================================
from util._serializers.state import State as Serializer
from util._models.state import State as Model
from util._views.change_log import ChangeLog

# =====================================================================


class State(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
