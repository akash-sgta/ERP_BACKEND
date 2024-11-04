# =====================================================================
from django.contrib import admin

# =====================================================================


class Company(admin.ModelAdmin):
    list_display = ("is_active",) + ("name",)
    list_filter = ("is_active",) + ("name",)
    readonly_fields = (
        "is_active",
        "createdOn",
        "createdBy",
        "changedOn",
        "changedBy",
    )
    search_fields = ("name",)
