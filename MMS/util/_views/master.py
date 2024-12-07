# =====================================================================
from util._serializers.master import Master as Serializer
from util._models.master import Master as Model
from util._views.change_log import ChangeLog

# =====================================================================


class Master(ChangeLog):
    """
    Master APIView to handle CRUD operations inherited from ChangeLog model.

    This class inherits from ChangeLog and reuses its functionality for CRUD operations.

    Attributes:
    - serializer_class: Serializer class used for validating and serializing data.
    - model: The model associated with this APIView.
    """

    serializer_class = Serializer
    model = Model
