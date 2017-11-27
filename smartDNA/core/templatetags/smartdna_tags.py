import itertools
from django import template
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import NoReverseMatch, reverse
from django.db.models import ForeignKey
from django.template.defaulttags import NowNode
from django.utils.safestring import mark_safe
from suit.config import get_config
from suit import utils
from subprocess import Popen, PIPE
import os
#import subprocess

from core.models import Logger

try:
    # Django 1.9
    from django.contrib.admin.utils import lookup_field
except ImportError:
    from django.contrib.admin.util import lookup_field

PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]

register = template.Library()
def get_version():
    #gitproc = Popen(['git', 'tag'], stdout = PIPE)
    gitproc = Popen(['git', 'tag'], stdout = PIPE,cwd=PROJECT_PATH)
    (stdout, stderr) = gitproc.communicate()
    #label=subprocess.check_output(["git", "tag"])
    return stdout.strip().splitlines()[-1]#[5:]#label.strip()

@register.filter(name='site_title')
def site_title(name):
    value= get_config(name)
    return mark_safe(value)[:28]+"..." if isinstance(value, str) else value

@register.simple_tag
def app_version():
    #print get_version()
    return get_version()

@register.simple_tag
def last_login_details():
    login_records = Logger.objects.all().order_by("-login_time")
    if login_records.count()>1:
       last_login_user= login_records[1].user
       last_login_time= login_records[1].login_time.strftime("%B %d, %Y - %r")
       #last_login_time= login_records[1].login_time.strftime("%B %d, %Y - %I:%M %p")
       return 'Last Login by: <strong style="color:#ff6d02">%s</strong> at <strong style="color:#ff6d02">%s</strong>'%(last_login_user,last_login_time)
    else:
       return ''

@register.simple_tag
def current_user (user):
    if user is str('admin'):
        show_settings=True
        print "Show setting to ", user, show_settings
        return show_settings
    else:
        show_settings=False
        print "Show setting to ",user,show_settings
        return show_settings



