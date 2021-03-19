"""
WSGI config for dprojx project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os
import dotenv
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dprojx.settings')
dotenv.load_dotenv(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')
)
application = get_wsgi_application()

