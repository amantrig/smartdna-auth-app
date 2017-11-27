__author__ = 'linksmart'
from django.contrib.gis.geoip import GeoIP
from django.contrib.auth import authenticate
from .models import Logger# your simple Log model
from .forms import LoginForm

def get_ip(request):
   xff = request.META.get('HTTP_X_FORWARDED_FOR')
   if xff:
      return xff.split(',')[0]
   return request.META.get('REMOTE_ADDR')

class UserLocationLoggerMiddleware(object):
    def process_request(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            usrname = form.cleaned_data['username']
            passwd = form.cleaned_data['password']
            user = authenticate(username=usrname,password=passwd)
            if user is not None:
                user_agent=request.META.get('HTTP_USER_AGENT').split('/')[0].lower()
                print 'user agent-  ',user_agent
                if user_agent == 'curl' or user_agent == 'linksmart':
                    print 'API login'
                else:
                    print 'PORTAL login'
                    try:
                        ip = get_ip(request)
                        print(ip)
                        g = GeoIP()
                        c = g.city(ip)
                        c1={"user":user,"city":c['city'],"postal_code":c['postal_code'],"country_name":c['country_name'],"country_code":c['country_code'],"ip_address":ip}
                        m = Logger(**c1)
                        m.save()
                    except:
                        print "exception in GeoIP block"

