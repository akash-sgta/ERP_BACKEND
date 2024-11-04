# =====================================================================
from profile._serializers.profile import Profile as Serializer
from profile._models.profile import Profile as Model
from util._views.master import Master

# =====================================================================


class Profile(Master):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
