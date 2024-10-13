# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class File(ChangeLog):
    list_display = (
        "name",
        "type",
    )
    list_filter = ("type",)
    search_fields = ("name",)
