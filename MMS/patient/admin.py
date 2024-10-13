# =====================================================================
from django.contrib import admin
from patient._admins.patient import Patient as Admin_Patient_Patient
from patient._models.patient import Patient as Model_Patient_Patient

# =====================================================================

admin.site.register(Model_Patient_Patient, Admin_Patient_Patient)
