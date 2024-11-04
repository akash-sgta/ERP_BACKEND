# =====================================================================
from util._admins.master import Master

# =====================================================================


class District(Master):
    list_display = Master.list_display + ("name",)
    list_filter = Master.list_filter + ("state",)
    search_fields = Master.search_fields + ("name",)
