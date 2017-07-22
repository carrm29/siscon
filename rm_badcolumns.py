from apps.registros.models import *

import os, sys
from shutil import move
from django.db import connection


tables = connection.introspection.table_names()
seen_models = connection.introspection.installed_models(tables)

errorColumn = []

for model in seen_models:
    try:
        model.objects.all()
    except:
        errorColumn.append(str(sys.exc_info()[1])[30::]+' =')
        #this weird expression just get the column that causes trouble
        #you may have to adapt indexes depending on error output in exc_info

os.chdir('./pvrep/')

#removing columns from models.py based on the error pattern
def replace(pattern, subst):
    with open('models_sub.py','w') as fout:
        with open('models.py','r') as models:
            for line in models:
                fout.write(line.replace(pattern, subst))

    os.remove('models.py')
    move('models_sub.py','models.py')

#applying this func to each error, and commenting out columns with an error mark to catch them back later
for errorStr in errorColumn:
    replace(errorStr, '#error_mark '+errorStr)

print 'Removiendo la  columna problemática patra volver a entrar..'
