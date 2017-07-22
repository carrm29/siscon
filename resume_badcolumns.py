from apps.registros.models import *

import os, sys
from shutil import move
from django.db import connection


os.chdir('./pvrep/')

#same search and replace func but returning True if sthg was replaced, and False otherwise
def replace(pattern, subst):
    a = False
    with open('models_sub.py','w') as fout:
        with open('models.py','r') as models:
            for line in models:
                fout.write(line.replace(pattern, subst))
                if pattern in line:
                    a = True
    os.remove('models.py')
    move('models_sub.py','models.py')

    return a

a = True
#while error_marks are replaced, we go on looping
while a:
    a = replace('#error_mark ', '')

print 'Voviendo a agregar las columnas que estaban mal..'