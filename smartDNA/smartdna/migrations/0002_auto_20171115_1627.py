# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartdna', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registration',
            name='child_of',
            field=models.CharField(default=b'', max_length=32, verbose_name=b'Parent Asset-ID '),
        ),
        migrations.AddField(
            model_name='verification',
            name='child_of',
            field=models.CharField(default=b'', max_length=32, verbose_name=b'Parent Asset-ID '),
        ),
    ]
