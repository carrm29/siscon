from apps.registros.models import *

import os, sys
from shutil import move

from django.db import connection

tables = connection.introspection.table_names()
seen_models = connection.introspection.installed_models(tables)

errorColumn = []
is_fine = "Todo se ve bien!"
#looping through models to detect issues
for model in seen_models:
    try:
        print(model.objects.all())
    except:
        is_fine = "WARNING algunos modelos estan corruptos"

print(is_fine)