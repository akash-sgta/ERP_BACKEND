# =====================================================================
from util._admins.master import Master

# =====================================================================


class File(Master):
    list_display = Master.list_display + (
        "name",
        "type",
    )
    list_filter = Master.list_filter + ("type",)
    search_fields = Master.search_fields + ("name",)
