"""
WSGI config for MERCES project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

sys.path.append(os.environ.get("MERCES_PROJECT_DIR") + "/merces")
sys.path.append(os.environ.get("MERCES_PROJECT_DIR") + "/merces/MERCES")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MERCES.settings.staging")

application = get_wsgi_application()
