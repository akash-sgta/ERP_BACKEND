# =====================================================================
import logging
import os

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import Settings, settings


# =====================================================================


@require_http_methods(["GET"])
def logger_view(request):
    html_script = str()
    file_path = os.path.join(settings.BASE_DIR, "logfile.log")
    with open(file_path, "r") as file:
        for line in file:
            html_script = "{}<br>{}".format(html_script, line.strip())
    html_script = "<html>{}</html>".format(html_script)
    return HttpResponse(html_script)
