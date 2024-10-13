# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Country(ChangeLog):
    list_display = ("name",)
    list_filter = ("continent__name",)
    search_fields = ("name",)
