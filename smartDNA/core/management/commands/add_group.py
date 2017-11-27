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
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models.loading import get_model

def add_group(dep_name,group_name,permissions_json):
    new_group, created = Group.objects.get_or_create(name=group_name)
    permissions = Permission.objects.filter(content_type__app_label=dep_name)
    with open(PROJECT_PATH+'smartDNA/'+permissions_json) as permissions_data:
    	data = json.load(permissions_data)

    for action in data[dep_name]:
	for model_name in data[dep_name][action]:
    	    model = get_model(dep_name, model_name)
	    model_verbose_name = model._meta.verbose_name.title()
	    try:
	     model_verbose_name = model._meta.verbose_name_plural.title()
	    except:
	     model_verbose_name=model_name._meta.verbose_name.title()
    	    cn = '%s_%s'%(action,model_name.lower())
    	    pn = 'Can %s %s'%(action,model_verbose_name)
    	    ct = ContentType.objects.get_for_model(model)
    	    #permission = Permission.objects.get(codename=cn,name=pn,content_type=ct)
	    for permission in permissions:
	     if permission.codename==cn:
	      new_group.permissions.add(permission)
	      break
             print permission.name

class Command(BaseCommand):
    help = 'Create group with specified permissions'
    def add_arguments(self, parser):
        parser.add_argument('dep_name')
        parser.add_argument('group_name')
        parser.add_argument('permissions_json')
    def handle(self, *args, **options):
        dep_name = options['dep_name']
        group_name = options['group_name']
        permissions_json = options['permissions_json']
        add_group(dep_name,group_name,permissions_json)

