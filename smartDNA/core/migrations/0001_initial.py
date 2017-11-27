# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0006_require_contenttypes_0002'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(null=True, verbose_name='last login', blank=True)),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, max_length=30, validators=[django.core.validators.RegexValidator('^[\\w.@+-]+$', 'Enter a valid username. This value may contain only letters, numbers and @/./+/-/_ characters.', 'invalid')], help_text='Required. 30 characters or fewer. Letters, digits and @/./+/-/_ only.', unique=True, verbose_name='username')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(max_length=254, verbose_name='email address', blank=True)),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dep_user', models.CharField(max_length=32, verbose_name=b'Deployment User')),
                ('dep_type', models.CharField(max_length=32, verbose_name=b'Deployment Type')),
                ('email_host', models.CharField(max_length=128, verbose_name=b'Email Host')),
                ('email_user', models.CharField(max_length=64, verbose_name=b'Email User')),
                ('email_pass', models.CharField(max_length=64, verbose_name=b'Email Pass')),
                ('email_port', models.IntegerField(default=465, verbose_name=b'Email Port')),
                ('cleanup_interval', models.IntegerField(default=90, verbose_name=b'Cleanup Interval')),
            ],
        ),
        migrations.CreateModel(
            name='Deployment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_type', models.CharField(default=b'Auditor', max_length=32, verbose_name=b'User Type', choices=[(b'Auditor', b'Auditor'), (b'Operator', b'Operator'), (b'Vendor', b'Vendor')])),
                ('dep_name', models.CharField(default=b'', max_length=32, verbose_name=b'Deployment Name')),
                ('dep_path', models.CharField(default=b'', max_length=32, verbose_name=b'Deployment Path')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Logger',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('login_time', models.DateTimeField(auto_now=True, verbose_name=b'Login Time')),
                ('user', models.CharField(max_length=32, verbose_name=b'User')),
                ('city', models.CharField(max_length=32, null=True, verbose_name=b'City', blank=True)),
                ('postal_code', models.CharField(max_length=32, null=True, verbose_name=b'Postal Code', blank=True)),
                ('country_name', models.CharField(max_length=32, null=True, verbose_name=b'Country', blank=True)),
                ('country_code', models.CharField(max_length=32, null=True, verbose_name=b'Country Code', blank=True)),
                ('ip_address', models.CharField(max_length=32, null=True, verbose_name=b'IP Address', blank=True)),
            ],
            options={
                'verbose_name_plural': 'User Login Records',
            },
        ),
        migrations.AddField(
            model_name='configuration',
            name='dep_name',
            field=models.OneToOneField(to='core.Deployment'),
        ),
    ]
