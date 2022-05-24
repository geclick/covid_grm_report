"""
WSGI config for MERCES project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""

from whitenoise import WhiteNoise

from . import wsgi

application = wsgi()
application = WhiteNoise(application, root="/app/static")
application.add_files("/app/assets", prefix="more-files/")
