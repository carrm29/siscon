# from django.conf import settings
from django.contrib.admin import forms
from django import forms

import locale

locale.setlocale (locale.LC_ALL, '')


class CargarExcelForm (forms.Form):
    # filename = forms.CharField(max_length=100)
    docfile = forms.FileField (label='Selecciona el archivo de la empresa', )

    docfileprov = forms.FileField (label='Selecciona el archivo del provedor')

    # Combo-box para el tipo de venta
    VTAS_1 = 'IVA'
    VTAS_2 = 'SIVA'
    VTAS_CHOICES = ((VTAS_1, u"Sin IVA"), (VTAS_2, u"Con IVA"))

    vtasiva = forms.ChoiceField (choices=VTAS_CHOICES, label='Tipo de venta')
    # Fin del combo-box con valores fijos

    # Acepta el fomateo por que es  .DecimalField, si es .FloatField marca error
    porvta = forms.DecimalField (label='Ingresa el porcentaje a liquidar %', initial=0.00, min_value=0.00,
                                 max_value=100.00, max_digits=4, decimal_places=2, localize=True,
                                 error_messages={'max_digits': 'Demasiados digitos'})

    porvtasim = forms.DecimalField (label='Ingresa el porcentaje de SIM a liquidar %', initial=0.00, min_value=0.00,
                                    max_value=100.00, max_digits=4, decimal_places=2, localize=True,
                                    error_messages={'max_digits': 'Demasiados digitos'})

    porvtaporta = forms.DecimalField (label='Ingresa el porcentaje de PORTA a liquidar %', initial=0.00, min_value=0.00,
                                      max_value=100.00, max_digits=4, decimal_places=2, localize=True,
                                      error_messages={'max_digits': 'Demasiados digitos'})

# fecha = forms.DateField(input_formats=settings.DATE_INPUT_FORMATS)
