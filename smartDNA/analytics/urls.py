from django.conf.urls import patterns, url, include
from django.contrib.auth.decorators import login_required
from analytics import views
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
   #Portal Views
   url(r'^main/$',login_required(views.main),name='main'), 
   url(r'^get_latest/$',login_required(views.get_last_status),name='get_last_status'),
) 
