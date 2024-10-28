# =====================================================================
from profile._serializers.profile import Profile as Serializer
from profile._models.profile import Profile as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Profile(ChangeLog):

    queryset = Model.objects.all()
    serializer_class = Serializer
    model = Model
