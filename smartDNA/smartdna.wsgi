import os
import sys


os.environ['PYTHON_EGG_CACHE'] = "/tmp"
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH
if path not in sys.path:
    sys.path.append(path)

path = PROJECT_PATH+'smartDNA'
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
