# =====================================================================
from profile._serializers.address import Address as Serializer
from profile._models.address import Address as Model
from util._views.master import Master

# =====================================================================


class Address(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
