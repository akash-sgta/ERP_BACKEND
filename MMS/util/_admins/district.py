# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class District(ChangeLog):
    list_display = ChangeLog.list_display + ("name",)
    list_filter = ChangeLog.list_filter + ("state",)
    search_fields = ChangeLog.search_fields + ("name",)
