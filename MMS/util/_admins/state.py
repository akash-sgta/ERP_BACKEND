# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class State(ChangeLog):
    list_display = ("name",)
    list_filter = ("country",)
    search_fields = ("name",)
