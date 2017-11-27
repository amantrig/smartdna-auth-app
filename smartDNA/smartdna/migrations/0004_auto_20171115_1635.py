# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('smartdna', '0003_auto_20171115_1635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registration',
            name='child_of',
            field=models.CharField(default=b'', max_length=32, null=True, verbose_name=b'Parent Asset-ID ', blank=True),
        ),
    ]
