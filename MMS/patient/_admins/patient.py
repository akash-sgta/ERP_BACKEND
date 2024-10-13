# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Patient(ChangeLog):
    list_display = (
        "pid",
        "profile__first_name",
        "profile__last_name",
    )
    list_filter = ()
    search_fields = (
        "pid",
        "profile__first_name",
        "profile__last_name",
        "profile__email",
    )
    readonly_fields = ChangeLog.readonly_fields + ("id",)
