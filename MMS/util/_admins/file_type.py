# =====================================================================
from util._admins.master import Master

# =====================================================================


class FileType(Master):
    list_display = Master.list_display + (
        "code",
        "name",
    )
    list_filter = Master.list_filter + ()
    search_fields = Master.search_fields + (
        "code",
        "name",
    )
