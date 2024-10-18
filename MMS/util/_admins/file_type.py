# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class FileType(ChangeLog):
    list_display = ChangeLog.list_display + (
        "code",
        "name",
    )
    list_filter = ChangeLog.list_filter + ()
    search_fields = ChangeLog.search_fields + (
        "code",
        "name",
    )
