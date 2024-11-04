# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Master(ChangeLog):
    list_display = ChangeLog.list_display + ("company",)
    list_filter = ChangeLog.list_filter + ("company",)
    search_fields = ChangeLog.search_fields + ("company",)
