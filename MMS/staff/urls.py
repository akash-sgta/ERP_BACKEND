# =====================================================================
from django.urls import re_path, include
from staff._views.doctor import Doctor
from staff._views.doctor_heirarchy import DoctorHierarchy
from staff._views.nurse import Nurse


# =====================================================================
PATTERN_ID = "(?P<id>\d*)"

urlpatterns = [
    re_path(
        rf"doctor/{PATTERN_ID}$",
        Doctor.as_view(),
        name="staff__doctor",
    ),
    re_path(
        rf"doctor_heirarchy/{PATTERN_ID}$",
        DoctorHierarchy.as_view(),
        name="staff__doctor_heirarchy",
    ),
    re_path(
        rf"nurse/{PATTERN_ID}$",
        Nurse.as_view(),
        name="staff__nurse",
    ),
    # re_path(r"signup/$", ff, name="signup"),
]
