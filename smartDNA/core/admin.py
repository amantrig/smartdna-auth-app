import datetime
from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from core.models import Deployment,Logger,Configuration,CustomUser
from core.forms import ConfigurationForm,CustomUserCreationForm, CustomUserChangeForm, CustomAdminPasswordChangeForm

class DeploymentAdmin(admin.ModelAdmin):
    list_display = ('user','user_type','dep_name','dep_path',)
    ordering = ('-id',)
    list_filter    = ('dep_name','user_type',)
    search_fields  = ('user',)

    def changelist_view(self, request, extra_context=None):
        try:
            page_title=Deployment._meta.verbose_name_plural.title()
            ctx={'title':page_title}
            return super(DeploymentAdmin, self).changelist_view(request, extra_context=ctx)
        except:
            page_title = Deployment._meta.verbose_name.title()
            ctx = {'title': page_title}
            return super(DeploymentAdmin, self).changelist_view(request, extra_context=ctx)

class LoggerAdmin(admin.ModelAdmin):
    list_display = ('user','login_time','city','country_name','country_code','postal_code','ip_address')
    ordering = ('-login_time',)
    list_filter    = ('city','country_name')
    search_fields  = ('country_name',)

    def changelist_view(self, request, extra_context=None):
        try:
            page_title=Logger._meta.verbose_name_plural.title()
            ctx={'title':page_title}
            return super(LoggerAdmin, self).changelist_view(request, extra_context=ctx)
        except:
            page_title = Logger._meta.verbose_name.title()
            ctx = {'title': page_title}
            return super(LoggerAdmin, self).changelist_view(request, extra_context=ctx)

class ConfigurationAdmin(admin.ModelAdmin):
    list_display = ('dep_name','dep_user','dep_type','email_host','email_user','email_port','cleanup_interval')
    ordering = ('-id',)
    list_filter    = ('dep_name','dep_user',)
    search_fields  = ('dep_name',)
    form = ConfigurationForm
    def changelist_view(self, request, extra_context=None):
        try:
            page_title = Configuration._meta.verbose_name_plural.title()
            ctx={'title':page_title}
            return super(ConfigurationAdmin, self).changelist_view(request, extra_context=ctx)
        except:
            page_title = Configuration._meta.verbose_name.title()
            ctx = {'title': page_title}
            return super(ConfigurationAdmin, self).changelist_view(request, extra_context=ctx)

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    change_password_form = CustomAdminPasswordChangeForm
    list_display = ('username', 'email', 'is_staff')

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
        ),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Deployment,DeploymentAdmin)
admin.site.register(Logger,LoggerAdmin)
admin.site.register(Configuration,ConfigurationAdmin)
