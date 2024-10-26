# =====================================================================
from util._serializers.country import Country as Serializer
from util._models.country import Country as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Country(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
