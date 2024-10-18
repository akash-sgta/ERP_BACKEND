# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class State(ChangeLog):
    list_display = ChangeLog.list_display + ("name",)
    list_filter = ChangeLog.list_filter + ("country",)
    search_fields = ChangeLog.search_fields + ("name",)
