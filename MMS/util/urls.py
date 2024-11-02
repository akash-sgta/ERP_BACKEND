# =====================================================================
from django.urls import re_path, include
from util._views.continent import Continent
from util._views.country import Country
from util._views.state import State
from util._views.district import District
from util._views.file_type import FileType
from util._views.file import File
from util._views.government_id_type import GovernmentIdType
from util._views.iso import Iso
# =====================================================================
PATTERN_ID = "(?P<id>\d*)"

urlpatterns = [
    re_path(
        rf"continent/{PATTERN_ID}",
        Continent.as_view(),
        name="util__continent",
    ),
    re_path(
        rf"country/{PATTERN_ID}",
        Country.as_view(),
        name="util__country",
    ),
    re_path(
        rf"state/{PATTERN_ID}",
        State.as_view(),
        name="util__state",
    ),
    re_path(
        rf"district/{PATTERN_ID}",
        District.as_view(),
        name="util__district",
    ),
    re_path(
        rf"file_type/{PATTERN_ID}",
        FileType.as_view(),
        name="util__file_type",
    ),
    re_path(
        rf"file/{PATTERN_ID}",
        File.as_view(),
        name="util__file",
    ),
    re_path(
        rf"government_id_type/{PATTERN_ID}",
        GovernmentIdType.as_view(),
        name="util__government_id_type",
    ),
    re_path(
        rf"iso/{PATTERN_ID}",
        Iso.as_view(),
        name="util__iso",
    ),
    # re_path(r"signup/$", ff, name="signup"),
]
