from django.conf.urls import patterns, include, url
from django.contrib.auth.views import password_reset

from .views import NuevoUsuario,Perfil,ActualizarPerfil,CambiarClave,register_confirm,Gracias
from django.contrib.auth import views as auth_views

urlpatterns = patterns('',

    #registro de usuarios nuevos
	url(r'^usuario-nuevo/$', 'apps.usuarios.views.NuevoUsuario', name="registrar-usuario"), #asi se asi anteriormente

    #Se envia un email para cambiar la clave, por olvido y no puede ingresar
    #url(r'^obtener-clave/$', 'apps.usuarios.views.ObtenerClave', name="reset-clave"),

    url(r'^password_reset/$', auth_views.password_reset,
        {'template_name': 'usuarios/obtenerClave.html'}, name='password_reset'),

    url(r'^password_reset/done/$', auth_views.password_reset_done,
        {'template_name': 'usuarios/password_reset_done.html'}, name= 'password_reset_done'),

    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.password_reset_confirm,
        {'template_name': 'usuarios/password_reset_confirm.html'}, name= 'password_reset_confirm'),
    url(r'^reset/done/$', auth_views.password_reset_complete,
        {'template_name': 'usuarios/password_reset_complete.html'}, name='password_reset_complete'),

    #Se cambia la clave estando logeado
    url(r'^cambiar-claveM/$', 'apps.usuarios.views.CambiarClaveM', name="chg-claveM"),


     #Marca errror
    #url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'usuarios/password_reset_email.html'}, name='password_reset'),


	#url(r'^perfil/$', 'apps.usuarios.views.Perfil', name="perfil"),
	#url(r'^perfil/actualizar-perfil/(?P<id_user>\d+)/$', 'apps.usuarios.views.ActualizarPerfil', name="actulizar-perfil"),
	#url(r'^perfil/cambiar-clave/$', 'apps.usuarios.views.CambiarClave', name="cambiar-clave"),
	#url(r'^confirmar/(?P<activation_key>\w+)/$', 'apps.usuarios.views.register_confirm', name="confirmar-correo"),

	url(r'^gracias/$', 'apps.usuarios.views.Gracias', name="cambiar-clave"),
    url(r'^gracias_rec/$', 'apps.usuarios.views.GraciasRec', name="solicitar-clave"),

)