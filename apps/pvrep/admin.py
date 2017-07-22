from django.contrib import admin
from .models import ArchivoEx, ArchivoExDet, ArchivoExProv, ArchivoExDetProv, ArchivoExDetLP, ArchivoExDetLNOP

admin.site.register(ArchivoEx)
admin.site.register(ArchivoExDet)

admin.site.register(ArchivoExProv)
admin.site.register(ArchivoExDetProv)

admin.site.register(ArchivoExDetLP)
admin.site.register(ArchivoExDetLNOP)
