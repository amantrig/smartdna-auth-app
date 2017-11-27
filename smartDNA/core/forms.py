import datetime
import os,json
import phonenumbers
from django.contrib.admin.forms import AdminAuthenticationForm
from django.core.exceptions import ValidationError
from django.core import validators
from django import forms
from django.contrib.admin.helpers import ActionForm
from django.contrib.admin.sites import AdminSite
from django.core.validators import RegexValidator
from phonenumber_field.formfields import PhoneNumberField
from django.forms import ModelForm
from core.models import Configuration, CustomUser
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext, ugettext_lazy as _
from core.utils import email_password

PROJECT_PATH=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
ALERT_CHOICE=(
        (1,"Tamper Alert"),
        (2,"Periodic Scan Alert"),
        (3,"Suspicious Duplication Alert")
        )

def validate_file_extension(value):
    import os
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.xlsx', '.xls']
    if not ext.lower() in valid_extensions:
        raise ValidationError(u'Unsupported file format.')

class ConfigurationForm(forms.ModelForm):
    email_pass = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = Configuration
        fields = ['dep_name','dep_user','dep_type','email_host','email_user','email_pass','email_port','cleanup_interval']

class PhoneField(forms.Field):
    default_error_messages = {
        'not_a_number': u'please provide correct number with country code e.g.:+917733230990',
    }
    def to_python(self, uvalue):
       if uvalue in validators.EMPTY_VALUES:
        return None
       value=str(uvalue)
       try:
        x = phonenumbers.parse(value, None)
        print phonenumbers.is_possible_number(x)
        print phonenumbers.is_valid_number(x)
        isvalid=phonenumbers.is_valid_number(x)
        if isvalid:
         return value
        else:
         raise ValidationError(self.error_messages['not_a_number'])
       except:
        raise ValidationError(self.error_messages['not_a_number'])


class LoginForm(forms.Form):
  username = forms.CharField(max_length=64)
  password = forms.CharField(max_length=64)
  #auth = forms.CharField(max_length=64)

class TrackTraceCheckForm(forms.Form):
  username= forms.CharField(max_length=64)
  password= forms.CharField(max_length=64)
  scan_auth= forms.CharField(max_length=64)
  email_id= forms.CharField(max_length=64)
  company_name= forms.CharField(max_length=64)

class CheckForm(forms.Form):
  asset_code= forms.CharField(max_length=64)
  scan_time= forms.CharField(max_length=64)
  credential= forms.CharField(max_length=128)
  orrcredential= forms.CharField(max_length=32)
  d1= forms.CharField(max_length=8)
  d2= forms.CharField(max_length=8)
  d3= forms.CharField(max_length=8)
  h1=forms.CharField(max_length=8)
  h2=forms.CharField(max_length=8)
  h3=forms.CharField(max_length=8)
  angle= forms.CharField(max_length=8)
  status= forms.CharField(max_length=64)
  operator= forms.CharField(max_length=64)
  location= forms.CharField(max_length=128)
  scan_auth= forms.CharField(max_length=64)
  scan_time= forms.CharField(max_length=64)
  email_id= forms.CharField(max_length=64)
  bit_mask= forms.CharField(max_length=128)
  company_name= forms.CharField(max_length=64)
  color_profile= forms.CharField(max_length=64)

class OrrCheckForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)
    asset_code= forms.CharField(max_length=64)
    orrStatus= forms.CharField(max_length=64)

class AnomalyForm(forms.Form):
    username = forms.CharField(max_length=64)
    password = forms.CharField(max_length=64)
    asset_code= forms.CharField(max_length=64)
    operator= forms.CharField(max_length=64)
    location= forms.CharField(max_length=64)

class FetchForm(forms.Form):
  username = forms.CharField(max_length=64)
  password= forms.CharField(max_length=64)
  asset_code= forms.CharField(max_length=64)
  company_name=forms.CharField(max_length=64)

class UpdateDetailsForm(forms.Form):
    username = forms.CharField(max_length=16)
    password = forms.CharField(widget=forms.PasswordInput)
    asset_code1 = forms.CharField(label='Asset Code(Sart)',max_length=16)
    asset_code2 = forms.CharField(label='Asset Code(End)',max_length=16)
    product_details = forms.CharField(max_length=64)
#,initial='example:product name,mfg date,exp date,batch no.'

class UpdateProductDetailsForm(forms.Form):
    STATIC, DYNAMIC = 'static', 'dynamic'
    UPDATE_METHOD_CHOICES = (
        (STATIC, 'Static'),
        (DYNAMIC, 'Import Excel (.xls, .xlsx)'),
    )
    update_method = forms.ChoiceField(choices=UPDATE_METHOD_CHOICES, widget=forms.RadioSelect,initial=STATIC)
    prefix =  forms.CharField(label='Prefix',max_length=8,required=False,
      widget=forms.TextInput(attrs={'placeholder':'max length: 8'}))
    start_id = forms.CharField(label='Start ID#',max_length=22,
      widget=forms.TextInput(attrs={'placeholder':'max length: 22 Integer only'}))
    end_id = forms.CharField(label='End ID#',max_length=22,
      widget=forms.TextInput(attrs={'placeholder':'max length: 22 Integer only'}))
    product_detail = forms.CharField(label='Product Detail',max_length=128,
      widget=forms.TextInput(attrs={'placeholder':'max length: 128'}))
    excel_file = forms.FileField(label='Excel File',required=False,validators=[validate_file_extension])

    def __init__(self, data=None, *args, **kwargs):
        super(UpdateProductDetailsForm, self).__init__(data, *args, **kwargs)

        # If dynamic is chosen, set filefield as required
        if data and data.get('update_method', None) == self.DYNAMIC:
            self.fields['excel_file'].required = True
            self.fields['start_id'].required = False
            self.fields['end_id'].required = False
            self.fields['product_detail'].required = False

class SettingsForm(forms.Form):
    with open(PROJECT_PATH+'smartDNA/media/settings.json', 'r') as f:
     json_data = json.load(f)
    #print json_data['dep_name'],json_data['dep_type']
    dep_name = forms.CharField(label='Deployment User',max_length=128,initial=json_data['dep_name'])
    dep_type = forms.CharField(label='Deployment Type',max_length=128,initial=json_data['dep_type'])
    email_host = forms.CharField(label='Email Host',max_length=128,initial=json_data['email_host'])
    email_port = forms.CharField(label='Email Port',max_length=128,initial=json_data['email_port'])
    email_username = forms.CharField(label='Email Username',max_length=128,initial=json_data['email_username'])
    email_password = forms.CharField(label='Email Password',max_length=128,initial=json_data['email_password'],widget=forms.PasswordInput(render_value=True))
    cleanup_interval=forms.CharField(label='Clean-up Interval',max_length=128,initial="90")

class DateRangeForm(forms.Form):
    day1 = forms.DateTimeField(initial=datetime.date.today()-datetime.timedelta(days=1),label="FROM")
    day2 = forms.DateTimeField(initial=datetime.date.today(),label="UPTO")
    status = forms.ChoiceField(label="Status",choices=(("Registration","Registration"),("Verification","Verification")))
    #widget = SelectDateWidget

class ScanAnalysisForm(forms.Form):
    day1 = forms.DateField(initial=datetime.date.today()-datetime.timedelta(days=30),label="FROM")
    day2 = forms.DateField(initial=datetime.date.today(),label="UPTO")
    scan_count=forms.IntegerField(initial=10,label="Scan Count")

class AssetCode_RangeForm(forms.Form):
      username = forms.CharField(label="Admin",initial='admin',max_length=16)
      password = forms.CharField(label='Password',widget=forms.PasswordInput,max_length=16)
      max_range = forms.CharField(label='Max Limit',max_length=16)

class BatchReportForm(forms.Form):
      batch_prefix = forms.CharField(label="Batch Prefix",initial='',max_length=16,required=False)
      first_batch_id = forms.CharField(label="Batch Start ID#",initial='',max_length=16)
      last_batch_id = forms.CharField(label="Batch End ID#",initial='',max_length=16)
      start_date = forms.DateField(initial=datetime.date.today()-datetime.timedelta(days=1),label="From")
      end_date = forms.DateField(initial=datetime.date.today(),label="To",)
      status = forms.ChoiceField(label="Status",choices=((1,"Registered"),(2,"Verified")))
      action = forms.ChoiceField(label="Action",choices=(("View","View"),("Download","Download (.xls)")))

class AdminDetailsForm(forms.Form):
    username = forms.CharField(label="Admin",max_length=16)
    password = forms.CharField(label="Password",widget=forms.PasswordInput)
    email_id= forms.EmailField(label="Email ID")
    mobile_number= PhoneField(label="Mobile Number")
    alert_type= forms.ChoiceField(label="Alert Type",choices=ALERT_CHOICE)

class OrrFilterForm(forms.Form):
    asset_code = forms.CharField(label="Asset Code",max_length=16)

class periodicScanSetterForm(forms.Form):
        username = forms.CharField(max_length=16)
        password = forms.CharField(widget=forms.PasswordInput)
        asset_code1 = forms.CharField(max_length=16)
        asset_code2 = forms.CharField(max_length=16)
        scanning_interval = forms.CharField(max_length=32,initial="4:30 hrs")

class DocumentForm(forms.Form):
      docfile = forms.FileField(label='Select a file',help_text='max. 42 megabytes')

class ScanIntervalForm(ActionForm):
      interval = forms.IntegerField(label='Scan Interval',widget=forms.TextInput(attrs={'placeholder': 'Interval in hours, e.g: 4.','id' : 'interval_field'}))

class CustomUserCreationForm(forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    password1 = forms.CharField(label=_("Password"),
        widget=forms.PasswordInput)
    password2 = forms.CharField(label=_("Password confirmation"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."))

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        eml = self.cleaned_data["email"]
        usrname = self.cleaned_data["username"]
        passwrd = self.cleaned_data["password1"]
        user.set_password(passwrd)
        if commit:
            user.save()
        print "user details ",eml,usrname,passwrd
        email_password(eml,usrname,passwrd)
        return user


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(label=_("Password"),
        help_text=_("Raw passwords are not stored, so there is no way to see "
                    "this user's password, but you can change the password "
                    "using <a href=\"password/\">this form</a>."))

    class Meta:
        model = CustomUser
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)
        f = self.fields.get('user_permissions', None)
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]

class CustomAdminPasswordChangeForm(forms.Form):
    """
    A form used to change the password of a user in the admin interface.
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    required_css_class = 'required'
    password1 = forms.CharField(
        label=_("Password"),
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label=_("Password (again)"),
        widget=forms.PasswordInput,
        help_text=_("Enter the same password as above, for verification."),
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(CustomAdminPasswordChangeForm, self).__init__(*args, **kwargs)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        """
        Saves the new password.
        """
        eml = self.user.email
        usrname = self.user.username
        passwrd = self.cleaned_data["password1"]
        self.user.set_password(self.cleaned_data["password1"])
        if commit:
            self.user.save()
        email_password(eml,usrname,passwrd)
        return self.user

    def _get_changed_data(self):
        data = super(CustomAdminPasswordChangeForm, self).changed_data
        for name in self.fields.keys():
            if name not in data:
                return []
        return ['password']
    changed_data = property(_get_changed_data)
