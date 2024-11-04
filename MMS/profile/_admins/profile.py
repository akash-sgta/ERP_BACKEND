# =====================================================================
from util._admins.master import Master

# =====================================================================


class Profile(Master):
    list_display = Master.list_display + (
        "first_name",
        "last_name",
    )
    list_filter = Master.list_filter + ()
    search_fields = Master.search_fields + (
        "first_name",
        "last_name",
    )
