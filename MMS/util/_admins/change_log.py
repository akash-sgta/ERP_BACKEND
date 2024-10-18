# =====================================================================
from django.contrib import admin

# =====================================================================


class ChangeLog(admin.ModelAdmin):
    list_display = ("is_active",)
    list_filter = ("is_active",)
    readonly_fields = (
        "is_active",
        "createdOn",
        "createdBy",
        "changedOn",
        "changedBy",
    )
