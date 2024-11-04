# =====================================================================
from util._serializers.country import Country as Serializer
from util._models.country import Country as Model
from util._views.master import Master

# =====================================================================


class Country(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
