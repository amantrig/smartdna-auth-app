from datetime import datetime, timedelta
from django.conf import settings
from django.contrib import auth


class AutoLogout:
  def process_request(self, request):
    if not request.user.is_authenticated() :
      #Can't log out if not logged in
      return

    try:
      #datetime.strptime(request.session['last_touch'],'%Y-%m-%dT%H:%M:%S.%f') 
      if datetime.now() - datetime.strptime(request.session['last_touch'],'%Y-%m-%d %H:%M:%S.%f')> timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        auth.logout(request)
        del request.session['last_touch']
        return
    except KeyError:
      pass

    request.session['last_touch'] = str(datetime.now())
