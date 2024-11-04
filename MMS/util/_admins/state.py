# =====================================================================
from util._admins.master import Master

# =====================================================================


class State(Master):
    list_display = Master.list_display + ("name",)
    list_filter = Master.list_filter + ("country",)
    search_fields = Master.search_fields + ("name",)
