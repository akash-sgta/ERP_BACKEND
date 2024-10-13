# =====================================================================
from django.contrib import admin
from util._admins.continent import Continent as Admin_Util_Continent
from util._models.continent import Continent as Model_Util_Continent
from util._admins.country import Country as Admin_Util_Country
from util._models.country import Country as Model_Util_Country
from util._admins.state import State as Admin_Util_State
from util._models.state import State as Model_Util_State
from util._admins.district import District as Admin_Util_District
from util._models.district import District as Model_Util_District
from util._admins.government_id_type import GovernmentIdType as Admin_Util_GovernmentIdType
from util._models.government_id_type import GovernmentIdType as Model_Util_GovernmentIdType
from util._admins.file_type import FileType as Admin_Util_FileType
from util._models.file_type import FileType as Model_Util_FileType
from util._admins.file import File as Admin_Util_File
from util._models.file import File as Model_Util_File

# =====================================================================

admin.site.register(Model_Util_Continent, Admin_Util_Continent)
admin.site.register(Model_Util_Country, Admin_Util_Country)
admin.site.register(Model_Util_State, Admin_Util_State)
admin.site.register(Model_Util_District, Admin_Util_District)
admin.site.register(Model_Util_GovernmentIdType, Admin_Util_GovernmentIdType)
admin.site.register(Model_Util_FileType, Admin_Util_FileType)
admin.site.register(Model_Util_File, Admin_Util_File)
