import os
import sys
from os.path import dirname, abspath
from django.core.wsgi import get_wsgi_application

from OpenEduSRE.settings import VIRTUALENV_PATH

os.environ["DJANGO_SETTINGS_MODULE"] = "OpenEduSRE.settings"
PROJECT_DIR = dirname(dirname(abspath(__file__)))
sys.path.insert(0, PROJECT_DIR)
sys.path.append(VIRTUALENV_PATH)
application = get_wsgi_application()
