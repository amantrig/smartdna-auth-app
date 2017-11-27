#0 8 * * 3 cd /home/ubuntu/linksmart/smartdna-auth-app/smartDNA && python manage.py update_geodb
import os
import sys
os.environ['PYTHON_EGG_CACHE'] = "/tmp"
path=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+"smartDNA/"
if path not in sys.path:
    sys.path.append(path)
os.environ['DJANGO_SETTINGS_MODULE'] = 'smartDNA.settings'

from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    help = 'Update GeoIP database (.dat file).'
    def handle(self, *args, **options):
        os.system('cd '+path+' && '+'wget "http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz"')
        os.system('cd '+path+' && '+'wget "http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz"')
        os.system('cd '+path+' && '+'gunzip -kf GeoIP.dat.gz')
        os.system('cd '+path+' && '+'gunzip -kf GeoLiteCity.dat.gz')
        os.system('cd '+path+' && '+'rm GeoIP.dat.gz')
        os.system('cd '+path+' && '+'rm GeoLiteCity.dat.gz')