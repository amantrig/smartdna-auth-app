import os, datetime
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import six, timezone
from django.contrib.auth.models import (
    BaseUserManager, AbstractUser
)

from core.utils import email_password

USER_CHOICES=(
    ('Auditor','Auditor'),
    ('Operator','Operator'),
    ('Vendor','Vendor'),
    )
#DEP_CHOICES=(
#)
#print filter(lambda x: os.path.isdir(os.path.join(os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+'smartDNA/', x)), os.listdir(os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]+'smartDNA/'))


class CustomUserManager(BaseUserManager):
    def _create_user(self, username, email, password,
                     is_staff, is_superuser, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,
                          date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        email_password(email,username,password)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        return self._create_user(username, email, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractUser):
    objects = CustomUserManager()
    class Meta:
      verbose_name_plural="Users"

class Logger(models.Model):
    login_time = models.DateTimeField(verbose_name="Login Time",blank=True,auto_now=True)
    user = models.CharField(verbose_name="User",max_length=32)
    city = models.CharField(verbose_name="City",max_length=32,null=True, blank=True)
    postal_code = models.CharField(verbose_name="Postal Code",max_length=32,null=True,blank=True,)
    country_name=models.CharField(verbose_name="Country",max_length=32,null=True,blank=True,)
    country_code=models.CharField(verbose_name="Country Code",max_length=32,null=True,blank=True,)
    ip_address=models.CharField(verbose_name="IP Address",max_length=32,null=True,blank=True,)
    class Meta:
	verbose_name_plural="User Login Records"


class Deployment(models.Model):  
    user = models.OneToOneField(CustomUser)  
    user_type=models.CharField(verbose_name="User Type",max_length=32,choices=USER_CHOICES, default="Auditor")
    dep_name = models.CharField(verbose_name="Deployment Name",max_length=32, default="")
    dep_path = models.CharField(verbose_name="Deployment Path",max_length=32, default="")

    def __str__(self):  
          return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = Deployment.objects.get_or_create(user=instance)  

post_save.connect(create_user_profile, sender=CustomUser)

class Configuration(models.Model):
      dep_name = models.OneToOneField(Deployment)
      dep_user = models.CharField(verbose_name="Deployment User",max_length=32)
      dep_type = models.CharField(verbose_name="Deployment Type",max_length=32)
      email_host = models.CharField(verbose_name="Email Host",max_length=128)
      email_user = models.CharField(verbose_name="Email User",max_length=64)
      email_pass = models.CharField(verbose_name="Email Pass",max_length=64)
      email_port = models.IntegerField(verbose_name="Email Port",default=465)
      cleanup_interval = models.IntegerField(verbose_name="Cleanup Interval",default=90)
