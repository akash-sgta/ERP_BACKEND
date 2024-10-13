# =====================================================================
from django.contrib import admin

# =====================================================================


class ChangeLog(admin.ModelAdmin):
    readonly_fields = (
        "createdOn",
        "createdBy",
        "changedOn",
        "changedBy",
    )
