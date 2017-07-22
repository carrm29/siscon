from django.conf.urls import patterns, include, url
from .views import upload_file

urlpatterns = patterns('',
    url(r'^cargar-excel/$', 'apps.pvrep.views.upload_file', name = 'cargar_excel'),
    url(r'^cargar-excel2/$', 'apps.pvrep.views.upload_file2', name = 'cargar_excel2'), #funciona bien, es sin parametros



	#url(r'^ver-notas-rapidas/$', NotaRapida.as_view(), name = 'nota_rapida'),
	#url(r'^modificarNota/$', ModificarNota.as_view(), name = 'modificar_nota'),
	#url(r'^eliminarNota/$', EliminarNota.as_view(), name = 'eliminar_nota'),
)