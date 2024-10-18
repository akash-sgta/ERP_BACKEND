# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Patient(ChangeLog):
    list_display = ChangeLog.list_display + (
        "profile__first_name",
        "profile__last_name",
    )
    list_filter = ChangeLog.list_filter + ()
    search_fields = ChangeLog.search_fields + (
        "profile__first_name",
        "profile__last_name",
        "profile__email",
    )
    readonly_fields = ChangeLog.readonly_fields + ()
