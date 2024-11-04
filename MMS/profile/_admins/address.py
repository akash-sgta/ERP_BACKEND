# =====================================================================
from util._admins.master import Master

# =====================================================================


class Address(Master):
    list_display = Master.list_display + (
        "line_01",
        "district",
        "post_office",
        "postal_code",
    )
    list_filter = Master.list_filter + (
        "district",
        "post_office",
        "postal_code",
    )
    search_fields = Master.search_fields + (
        "line_01",
        "line_02",
        "line_03",
        "line_04",
        "district__name",
        "post_office",
        "postal_code",
    )
