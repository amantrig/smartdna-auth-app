#!/usr/bin/env python
import os, sys

if __name__ == "__main__":
    path=os.path.dirname(os.path.realpath(__file__)).split("smartDNA")[0]
    if path not in sys.path:
     sys.path.append(path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "smartDNA.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)