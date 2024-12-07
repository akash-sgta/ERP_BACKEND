# =====================================================================
from django.urls import re_path, include
from patient._views.patient import Patient

# =====================================================================
PATTERN_ID = "(?P<id>\d*)"

urlpatterns = [
    re_path(
        rf"patient/{PATTERN_ID}$",
        Patient.as_view(),
        name="patient__patient",
    ),
    # re_path(r"signup/$", ff, name="signup"),
]
