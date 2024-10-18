# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Credential(ChangeLog):
    list_display = ChangeLog.list_display + ("user_name",)
    list_filter = ChangeLog.list_filter + ()
    search_fields = ChangeLog.search_fields + ("user_name",)
