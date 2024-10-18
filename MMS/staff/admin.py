# =====================================================================
from django.contrib import admin
from staff._admins.doctor import Doctor as Admin_Staff_Doctor
from staff._models.doctor import Doctor as Model_Staff_Doctor

# =====================================================================

admin.site.register(Model_Staff_Doctor, Admin_Staff_Doctor)
