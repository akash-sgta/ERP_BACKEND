# =====================================================================
from django.contrib import admin
from _user._admins.credential import Credential as Admin_User_Credential
from _user._models.credential import Credential as Model_User_Credential
from _user._admins.profile import Profile as Admin_User_Profile
from _user._models.profile import Profile as Model_User_Profile
from _user._admins.address import Address as Admin_User_Address
from _user._models.address import Address as Model_User_Address

# =====================================================================

admin.site.register(Model_User_Credential, Admin_User_Credential)
admin.site.register(Model_User_Profile, Admin_User_Profile)
admin.site.register(Model_User_Address, Admin_User_Address)
