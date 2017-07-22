from django.contrib.auth.models import User
from django.db import models


def generate_filename(self, filename):
    path_doctos = "docsexcel/%s/%s" % (self.usuario.username, filename)
    return path_doctos

class ArchivoEx(models.Model):
    filename = models.CharField(max_length=200, default="")
    numload = models.IntegerField()
    docfile = models.FileField(upload_to=generate_filename, default=False)
    fecha_r = models.DateField('Fecha de reg.', auto_now_add=True, auto_now=False)
    fecha_m = models.DateField('Fecha de act.', auto_now_add=False, auto_now=True)
    prodpor = models.CharField( max_length=200, default="" )
    usuario = models.ForeignKey(User)


    # El metodo __unicode_ es usado por Django por para mostrar un objecto en la interfaz
    # administrativa, como el valor insertado en la plantilla cuando muestra el objeto de
    # una forma que sea legible.
    # En Python 3 es __str__
    def __unicode__(self):
        return self.usuario.username

class ArchivoExDet(models.Model):
    DN = models.CharField(max_length=15, default="")
    ICC = models.CharField(max_length=30 , default="")
    FechaA = models.DateField(blank=True)
    Producto = models.CharField(max_length=20,  default="")
    Recarga = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Comision = models.DecimalField (default=0.00, max_digits=12, decimal_places=2)
    Estatus = models.CharField(max_length=20,  default="")
    filename = models.CharField(max_length=200, default="")
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario.username


class ArchivoExProv(models.Model):
    filename = models.CharField(max_length=200, default="")
    numload = models.IntegerField()
    docfile = models.FileField(upload_to=generate_filename, default=False)
    fecha_r = models.DateField('Fecha de reg.', auto_now_add=True, auto_now=False)
    fecha_m = models.DateField('Fecha de act.', auto_now_add=False, auto_now=True)
    usuario = models.ForeignKey(User)


    # El metodo __unicode_ es usado por Django por para mostrar un objecto en la interfaz
    # administrativa, como el valor insertado en la plantilla cuando muestra el objeto de
    # una forma que sea legible.
    # En Python 3 es __str__
    def __unicode__(self):
        return self.usuario.username

class ArchivoExDetProv(models.Model):
    DN = models.CharField(max_length=15, default="")
    ICC = models.CharField(max_length=30 , default="")
    FechaA = models.DateField(blank=True)
    Producto = models.CharField(max_length=20,  default="")
    Recarga = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Comision = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Estatus = models.CharField(max_length=20,  default="")
    filename = models.CharField(max_length=200, default="")
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario.username



class ArchivoExDetLP(models.Model):
    DN = models.CharField(max_length=15, default="")
    ICC = models.CharField(max_length=30 , default="")
    FechaA = models.DateField(blank=True)
    Producto = models.CharField(max_length=20,  default="")
    Recarga = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Comision = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    RecargaProv = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    ComisionProv = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Dif = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Estatus = models.CharField(max_length=20,  default="")
    filename = models.CharField(max_length=200, default="")
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario.username


class ArchivoExDetLNOP(models.Model):
    DN = models.CharField(max_length=15, default="")
    ICC = models.CharField(max_length=30 , default="")
    FechaA = models.DateField(blank=True)
    Producto = models.CharField(max_length=20,  default="")
    Recarga = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Comision = models.DecimalField(default=0.00, max_digits=12, decimal_places=2)
    Estatus = models.CharField(max_length=20,  default="")
    filename = models.CharField(max_length=200, default="")
    usuario = models.ForeignKey(User)

    def __unicode__(self):
        return self.usuario.username
