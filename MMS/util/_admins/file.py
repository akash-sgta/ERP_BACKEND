# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class File(ChangeLog):
    list_display = ChangeLog.list_display + (
        "name",
        "type",
    )
    list_filter = ChangeLog.list_filter + ("type",)
    search_fields = ChangeLog.search_fields + ("name",)
