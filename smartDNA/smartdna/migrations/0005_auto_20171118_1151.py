# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartdna', '0004_auto_20171115_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='asset_code',
            field=models.CharField(default=b'', unique=True, max_length=32, verbose_name=b'Asset-ID', db_index=True),
        ),
    ]
