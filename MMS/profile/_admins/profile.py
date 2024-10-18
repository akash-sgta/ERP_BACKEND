# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Profile(ChangeLog):
    list_display = ChangeLog.list_display + (
        "first_name",
        "last_name",
    )
    list_filter = ChangeLog.list_filter + ()
    search_fields = ChangeLog.search_fields + (
        "first_name",
        "last_name",
    )