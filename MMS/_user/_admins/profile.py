# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Profile(ChangeLog):
    list_display = (
        "first_name",
        "last_name",
    )
    list_filter = ()
    search_fields = (
        "first_name",
        "last_name",
    )
