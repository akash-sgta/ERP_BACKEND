# =====================================================================
from django.urls import re_path, include
from profile._views.address import Address
from profile._views.profile import Profile

# =====================================================================
PATTERN_ID = "(?P<id>\d*)"

urlpatterns = [
    re_path(
        rf"address/{PATTERN_ID}",
        Address.as_view(),
        name="profile__address",
    ),
    re_path(
        rf"profile/{PATTERN_ID}",
        Profile.as_view(),
        name="profile__profile",
    ),
    # re_path(r"signup/$", ff, name="signup"),
]
