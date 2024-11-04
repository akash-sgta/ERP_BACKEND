# =====================================================================
from util._admins.master import Master

# =====================================================================


class Doctor(Master):
    list_display = Master.list_display + (
        "profile__first_name",
        "profile__last_name",
    )
    list_filter = Master.list_filter + ()
    search_fields = Master.search_fields + (
        "profile__first_name",
        "profile__last_name",
        "profile__email",
    )
    readonly_fields = Master.readonly_fields + ()
