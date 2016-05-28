"""
WSGI config for ideascube project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ideascube.settings")
os.environ.setdefault("STORAGE_ROOT", "/var/ideascube")

from django.core.management import call_command
call_command('migrate', '--noinput', '-v', '1')
call_command('collectstatic', '--noinput', '-v', '1')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
