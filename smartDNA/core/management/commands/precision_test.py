import os
import sys
import json
os.environ['PYTHON_EGG_CACHE'] = "/tmp"
PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
path = PROJECT_PATH+'smartDNA/'
if path not in sys.path:
    sys.path.append(path)
path = PROJECT_PATH
sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'

from django.core.management.base import BaseCommand, CommandError
from core.model_utils import precision_test

class Command(BaseCommand):
    help = 'Get number of verifcation records under 0.4 precision'
    def add_arguments(self, parser):
        parser.add_argument('asset_code')
        parser.add_argument('dep_path')
        parser.add_argument('precision')
    def handle(self, *args, **options):
    	asset_code = options['asset_code']
        dep_path = options['dep_path']
        precision = options['precision']
    	precision_test(asset_code,dep_path,precision)
