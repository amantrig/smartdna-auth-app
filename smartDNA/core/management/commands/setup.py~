import os
import sys
import re

def get_path(): 
    smartdna_path=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+"smartDNA/"
    print smartdna_path
    '''smartdna_path=re.sub('smartDNA$', '', os.getcwd())
    print smartdna_path
    return smartdna_path'''

os.environ['PYTHON_EGG_CACHE'] = "/tmp"
path = os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+"smartDNA/"
if path not in sys.path:
    sys.path.append(path)
path = os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'setup smartDNA application'
    def handle(self, *args, **options):
        get_path()
	
