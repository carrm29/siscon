from django.contrib.auth import user_logged_in
from django.db import models
from django.contrib.auth.models import User
import datetime

from django.utils import timezone


class Perfiles(models.Model):
    nombre = models.CharField(max_length=20)
    apellido = models.CharField(max_length=25)
    telefono = models.IntegerField()
    correo = models.EmailField(max_length=70)
    activation_key = models.CharField(max_length=40, blank=True)
    date_key_expires = models.DateTimeField(default=timezone.now)
    usuario = models.OneToOneField(User)


    def update_last_login(sender, user, **kwargs):
        """
            A signal receiver which updates the last_login date for
            the user logging in.
        """
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])


    user_logged_in.connect(update_last_login)


    def __unicode__(self):
            return self.usuario.username


