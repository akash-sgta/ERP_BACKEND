# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class GovernmentIdType(ChangeLog):
    list_display = ("name",)
    list_filter = ()
    search_fields = ("name",)
