from django.conf.urls import patterns, include, url

from django.contrib.auth import views as auth_views
from django.contrib.auth.views import login, password_reset, password_change_done, password_reset_confirm, password_reset_complete

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'siscon.views.home', name='home'),
    # url(r'^siscon/', include('siscon.foo.urls')),

    url(r'^admin/', include(admin.site.urls)),

    #INICIO
    url(r'^', include('apps.inicio.urls')),#indicamos que vamos a usar la urls de inicio

    #REGISTROS
    url(r'^', include('apps.registros.urls')),

    #MENU
    url(r'^', include('apps.menu.urls')),

    #NUEVO_USUARIO
    url(r'^', include('apps.usuarios.urls')),
    #NOTAS RAPIDAS
    url(r'^', include('apps.notas.urls')),

    # PVREP
    url(r'^', include('apps.pvrep.urls')),

                       #No funcionan
    #url(r'^password_reset/$', auth_views.password_reset,{'template_name': 'usuarios/password_reset_email.html'}, name='password_reset'),
    #url(r'^password_reset/$', auth_views.password_reset, {'next_page': '/'}, name='password_reset'),

)