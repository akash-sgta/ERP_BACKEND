# =====================================================================
from django.contrib import admin
from profile._admins.profile import Profile as Admin_User_Profile
from profile._models.profile import Profile as Model_User_Profile
from profile._admins.address import Address as Admin_User_Address
from profile._models.address import Address as Model_User_Address

# =====================================================================

admin.site.register(Model_User_Profile, Admin_User_Profile)
admin.site.register(Model_User_Address, Admin_User_Address)
