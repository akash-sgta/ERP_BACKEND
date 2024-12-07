# =====================================================================
import logging
import os

from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.conf import Settings, settings


# =====================================================================


@require_http_methods(["GET"])
def logger_view(request):
    _limit = 100
    _file_path = os.path.join(settings.BASE_DIR, "logfile.log")
    log = list()
    try:
        with open(_file_path, "r") as file:
            lines = file.readlines()
            for line in reversed(lines):
                log.append(line.strip())
                _limit = _limit - 1
                if _limit <= 0:
                    break
            body = "<br>".join(log)
    except FileNotFoundError:
        body = "<h1>No Logs Found !</h1>"
    finally:
        style = "body { background-color: black; color: white; font-family: Arial, sans-serif; }"
        html_script = """
                        <html>
                            <head>
                                <style>
                                    {}
                                </style>
                            </head>
                            <body>
                                {}
                            </body>
                        </html>""".format(
            style, body
        )
    return HttpResponse(html_script)
