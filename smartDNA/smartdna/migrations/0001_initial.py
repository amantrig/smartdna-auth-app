# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ActivityLog',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('staff', models.CharField(default=b'', max_length=16, verbose_name=b'User')),
                ('activity_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Activity Time')),
                ('operator', models.CharField(default=b'NF', max_length=64, verbose_name=b'Operator')),
                ('ip_address', models.CharField(default=b'NF', max_length=16, verbose_name=b'IP Address')),
                ('city', models.CharField(default=b'NF', max_length=64, null=True, verbose_name=b'City', blank=True)),
                ('postal_code', models.CharField(default=b'NF', max_length=16, null=True, verbose_name=b'Postal COde', blank=True)),
                ('remark', models.CharField(default=b'NF', max_length=256, verbose_name=b'Remark')),
            ],
        ),
        migrations.CreateModel(
            name='Alert',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tracking_code', models.CharField(default=b'', max_length=32, verbose_name=b'Tracking Code')),
                ('alert_message', models.CharField(default=b'', max_length=64, verbose_name=b'Alert Message')),
                ('alert_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Scan Time')),
            ],
            options={
                'verbose_name_plural': 'Scan Alert',
            },
        ),
        migrations.CreateModel(
            name='AlertSubscriber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('subscriber', models.CharField(default=b'', max_length=32, verbose_name=b'Subscriber Name')),
                ('phone', models.CharField(default=b'', max_length=16, blank=True, help_text=b'optional', null=True, verbose_name=b'Mobile Number')),
                ('email', models.CharField(default=b'', max_length=64, verbose_name=b'Email ID')),
                ('scr_status', models.CharField(default=0, max_length=24, verbose_name=b'Subscription Status', choices=[(b'Active', b'Active'), (b'Inactive', b'Inactive')])),
            ],
            options={
                'verbose_name_plural': 'Alert Subscribers',
            },
        ),
        migrations.CreateModel(
            name='Anomaly',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_code', models.CharField(default=b'', max_length=32, verbose_name=b'Asset Code')),
                ('scan_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Time of smartDNA scan')),
                ('operator', models.CharField(default=b'NF', max_length=16, verbose_name=b'Operator')),
                ('location', models.CharField(default=b'NF', max_length=64, verbose_name=b'Location')),
            ],
            options={
                'verbose_name': 'Anomaly Record',
            },
        ),
        migrations.CreateModel(
            name='PeriodicScanAsset',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_code', models.CharField(default=b'', max_length=32, verbose_name=b'Asset ID')),
                ('interval', models.CharField(default=b'1', max_length=16, verbose_name=b'Scan Interval')),
            ],
        ),
        migrations.CreateModel(
            name='PostmortemImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_code', models.CharField(default=b'', max_length=32, verbose_name=b'Asset Code')),
                ('scan_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Time of Scan')),
                ('case_type', models.CharField(default=b'', max_length=32, verbose_name=b'Case')),
                ('result', models.CharField(default=b'Not Audited', max_length=64, verbose_name=b'Result', choices=[(b'Not Audited', b'Not Audited'), (b'Audited-OK', b'Audited-OK'), (b'Audited-Discrepant', b'Audited-Discrepant')])),
                ('imagefile', models.FileField(upload_to=b'postmortem_image/')),
            ],
            options={
                'verbose_name_plural': 'Postmortem Images',
            },
        ),
        migrations.CreateModel(
            name='Registration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_code', models.CharField(default=b'', max_length=32, verbose_name=b'Asset-ID', db_index=True)),
                ('scan_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Scan Time')),
                ('credential', models.CharField(default=b'', max_length=16, verbose_name=b'Credential')),
                ('d1', models.CharField(default=b'0.0', max_length=8, verbose_name=b'D1')),
                ('d2', models.CharField(default=b'0.0', max_length=8, verbose_name=b'D2')),
                ('d3', models.CharField(default=b'0.0', max_length=8, verbose_name=b'D3')),
                ('h1', models.CharField(default=b'0.0', max_length=8, verbose_name=b'H1')),
                ('h2', models.CharField(default=b'0.0', max_length=8, verbose_name=b'H2')),
                ('h3', models.CharField(default=b'0.0', max_length=8, verbose_name=b'H3')),
                ('angle', models.CharField(default=b'', max_length=8, verbose_name=b'Orientation')),
                ('status', models.IntegerField(default=1, db_index=True, verbose_name=b'Status', choices=[(1, b'Registered'), (2, b'Verified'), (3, b'Tampered'), (4, b'Tampered with line cut'), (5, b'Discrepant Label'), (6, b'Void'), (7, b'Barcode Error'), (8, b'Label Error'), (9, b'Height Error'), (10, b'Released'), (11, b'Audited'), (12, b'Unregistered'), (13, b'Verified-x'), (14, b'Tampered-2'), (15, b'Tampered-3')])),
                ('orr_credential', models.IntegerField(default=1000, verbose_name=b'Forensic Credential')),
                ('operator', models.CharField(default=b'', max_length=30, verbose_name=b'Operator', db_index=True)),
                ('geo_location', models.CharField(default=b'', max_length=64, verbose_name=b'Geo-Location')),
                ('street', models.CharField(default=b'', max_length=64, verbose_name=b'Address')),
                ('locality', models.CharField(default=b'', max_length=128, verbose_name=b'Locality')),
                ('city', models.CharField(default=b'', max_length=32, verbose_name=b'City')),
                ('state', models.CharField(default=b'', max_length=32, verbose_name=b'State')),
                ('postal_code', models.CharField(default=b'', max_length=16, verbose_name=b'Postal Code')),
                ('country', models.CharField(default=b'', max_length=16, verbose_name=b'Country')),
                ('auth_code', models.CharField(default=b'none', max_length=20, verbose_name=b'Mobile Number')),
                ('image', models.FileField(upload_to=b'documents/')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Created on')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'Modified on')),
                ('product_details', models.CharField(default=b'Not Found', max_length=128, null=True, verbose_name=b'Dispatch ID', blank=True)),
                ('bit_mask', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Bit Mask', blank=True)),
                ('color_profile', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Color Profile', blank=True)),
                ('email_id', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Recipient Email-ID', blank=True)),
                ('company_name', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Company', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Registrations',
            },
        ),
        migrations.CreateModel(
            name='Verification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('asset_code', models.CharField(default=b'', max_length=32, verbose_name=b'Asset-ID', db_index=True)),
                ('scan_time', models.DateTimeField(default=datetime.datetime.now, verbose_name=b'Scan Time')),
                ('credential', models.CharField(default=b'', max_length=16, verbose_name=b'Credential')),
                ('d1', models.CharField(default=b'0.0', max_length=8, verbose_name=b'D1')),
                ('d2', models.CharField(default=b'0.0', max_length=8, verbose_name=b'D2')),
                ('d3', models.CharField(default=b'0.0', max_length=8, verbose_name=b'D3')),
                ('h1', models.CharField(default=b'0.0', max_length=8, verbose_name=b'H1')),
                ('h2', models.CharField(default=b'0.0', max_length=8, verbose_name=b'H2')),
                ('h3', models.CharField(default=b'0.0', max_length=8, verbose_name=b'H3')),
                ('angle', models.CharField(default=b'', max_length=8, verbose_name=b'Orientation')),
                ('status', models.IntegerField(default=1, db_index=True, verbose_name=b'Status', choices=[(1, b'Registered'), (2, b'Verified'), (3, b'Tampered'), (4, b'Tampered with line cut'), (5, b'Discrepant Label'), (6, b'Void'), (7, b'Barcode Error'), (8, b'Label Error'), (9, b'Height Error'), (10, b'Released'), (11, b'Audited'), (12, b'Unregistered'), (13, b'Verified-x'), (14, b'Tampered-2'), (15, b'Tampered-3')])),
                ('orr_credential', models.IntegerField(default=1000, verbose_name=b'Forensic Credential')),
                ('operator', models.CharField(default=b'', max_length=30, verbose_name=b'Operator', db_index=True)),
                ('geo_location', models.CharField(default=b'', max_length=64, verbose_name=b'Geo-Location')),
                ('street', models.CharField(default=b'', max_length=64, verbose_name=b'Address')),
                ('locality', models.CharField(default=b'', max_length=128, verbose_name=b'Locality')),
                ('city', models.CharField(default=b'', max_length=32, verbose_name=b'City')),
                ('state', models.CharField(default=b'', max_length=32, verbose_name=b'State')),
                ('postal_code', models.CharField(default=b'', max_length=16, verbose_name=b'Postal Code')),
                ('country', models.CharField(default=b'', max_length=16, verbose_name=b'Country')),
                ('auth_code', models.CharField(default=b'none', max_length=20, verbose_name=b'Mobile Number')),
                ('image', models.FileField(upload_to=b'documents/')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=b'Created on')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name=b'Modified on')),
                ('product_details', models.CharField(default=b'Not Found', max_length=128, null=True, verbose_name=b'Dispatch ID', blank=True)),
                ('bit_mask', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Bit Mask', blank=True)),
                ('color_profile', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Color Profile', blank=True)),
                ('email_id', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Recipient Email-ID', blank=True)),
                ('company_name', models.CharField(default=b'', max_length=64, null=True, verbose_name=b'Company', blank=True)),
            ],
            options={
                'verbose_name_plural': 'Scan Monitoring',
            },
        ),
        migrations.AlterIndexTogether(
            name='verification',
            index_together=set([('company_name', 'modified', 'scan_time', 'id', 'status'), ('company_name', 'state', 'status', 'scan_time', 'id'), ('company_name', 'asset_code', 'product_details', 'auth_code', 'city', 'status', 'scan_time', 'id'), ('company_name', 'status', 'scan_time', 'id')]),
        ),
        migrations.AlterIndexTogether(
            name='registration',
            index_together=set([('company_name', 'modified', 'scan_time', 'id', 'status'), ('company_name', 'state', 'status', 'scan_time', 'id'), ('company_name', 'asset_code', 'product_details', 'auth_code', 'city', 'status', 'scan_time', 'id'), ('company_name', 'status', 'scan_time', 'id')]),
        ),
    ]
