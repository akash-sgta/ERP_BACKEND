# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Iso(ChangeLog):
    list_display = ChangeLog.list_display + ("code","country__name",)
    list_filter = ChangeLog.list_filter + ()
    search_fields = ChangeLog.search_fields + ("country__name",)
