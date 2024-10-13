# =====================================================================
from util._admins.change_log import ChangeLog

# =====================================================================


class Address(ChangeLog):
    list_display = (
        "line_01",
        "district",
        "post_office",
        "postal_code",
    )
    list_filter = (
        "district",
        "post_office",
        "postal_code",
    )
    search_fields = (
        "line_01",
        "line_02",
        "line_03",
        "line_04",
        "district__name",
        "post_office",
        "postal_code",
    )
