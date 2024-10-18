# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Continent(ChangeLog):
    list_display = ChangeLog.list_display + ("name",)
    list_filter = ChangeLog.list_filter + ()
    search_fields = ChangeLog.search_fields + ("name",)
