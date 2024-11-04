# =====================================================================
from util._admins.master import Master

# =====================================================================


class Country(Master):
    list_display = Master.list_display + ("name",)
    list_filter = Master.list_filter + ("continent__name",)
    search_fields = Master.search_fields + ("name",)
