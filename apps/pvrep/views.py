import xlrd as xlrd
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, render_to_response  # puedes importar render_to_response
from django.template import RequestContext
from apps.pvrep.forms import CargarExcelForm
from apps.pvrep.models import ArchivoEx, ArchivoExDet, ArchivoExProv, ArchivoExDetProv, ArchivoExDetLP, ArchivoExDetLNOP
from django.db.models import Count, Min, Sum, Avg

import datetime


# Librerias openpyxl, pero solo lee .xlsx
# from openpyxl import load_workbook
# from io import BytesIO


@login_required()
def upload_file(request):
    if request.method == 'POST':
        form = CargarExcelForm(request.POST, request.FILES)

        vnumload = ArchivoEx.objects.count() + 1  # asigno el numero de cargas, este no lo tomo de la pantalla
        vusername = request.user  # Obtengo el usuario de la sesion y lo asigno a la variable para ser salvado.

        # vfilename = request.FILES['docfile'] Solo funciona si en la pantalla se tecleo un valor, si viene
        # en blanco marca error.
        # Esta funciona y valida que se teclee algo en la pantalla
        vfilename = request.FILES.get("docfile", "Guest")
        vfilenameprov = request.FILES.get("docfileprov", "Guest")

        # Datos para calculos
        vvtaiva = request.POST.get("vtasiva", "Guest")
        vporvta = request.POST.get("porvta", "Guest")
        vporvtasim = request.POST.get("porvtasim", "Guest")
        vporvtaporta = request.POST.get ("porvtaporta", "Guest")


        vlprodpor='GEN' + ' ' + str (vporvta) + ' ' + 'SIM'+ ' ' + str (vporvtasim) + ' ' + 'PORTA' + ' ' + str (vporvtaporta)


        if form.is_valid():  # and vnumload < 5:

            # Leemos el archivo que esta en memoria
            file_in_memory = request.FILES['docfile'].read()
            file_in_memoryprov = request.FILES['docfileprov'].read()

            # openpyxl esta hecho para xlsx
            # Esta funcion solo carga archivos xlsx, si tratas de cargar xls marca error BadZipfile, "File is not a zip file"
            # wbook = load_workbook(filename=BytesIO(file_in_memory))
            # Como ya tenemos el apuntador de memoria wbook al archivo de excel, ya podemos
            # manipularlo
            # print(wbook.get_sheet_names())

            # xlrd lee archivos xls y xlsx
            wbook_xlrd = xlrd.open_workbook(file_contents=file_in_memory)
            wbook_xlrdprov = xlrd.open_workbook(file_contents=file_in_memoryprov)

            # Como ya tenemos el apuntador de memoria wbook al archivo de excel, ya podemos
            # manipularlo
            # print (wbook_xlrd.sheet_names()) imprime los nombres de las hojas

            # CARGO EL PRIMER ARCHIVO
            # Cargo la primera hora y veo en numero ded renglones
            vsheet = wbook_xlrd.sheet_by_index(0)
            nr_rows = vsheet.nrows

            # Elimino las tablas
            del_all = ArchivoEx.objects.filter(usuario=request.user.id)
            del_all.delete()
            del_all = ArchivoExDet.objects.filter(usuario=request.user.id)
            del_all.delete()
            del_all = ArchivoExProv.objects.filter(usuario=request.user.id)
            del_all.delete()
            del_all = ArchivoExDetProv.objects.filter(usuario=request.user.id)
            del_all.delete()
            del_all = ArchivoExDetLP.objects.filter(usuario=request.user.id)
            del_all.delete()
            del_all = ArchivoExDetLNOP.objects.filter(usuario=request.user.id)
            del_all.delete()

            # FINALIZO ELIMINAR TABLAS


            # Comenzamos en el renglon 2, el 1 son los encabezados
            first_row = 2  # nr_rows - 2
            for vrow in range(first_row, nr_rows):
                # print vsheet.row(vrow) #imprime el renglon completo en una tupla con los valores
                valsrow = []  # Preparo mi tupla para ir agregando los valores de c/renglon de excel
                for vcell in vsheet.row(vrow):
                    if vcell.ctype == 3:  # Del tipo 3 son las fechas
                        ms_date_number = vcell.value
                        # manejo de fechas de excel a modelos django-python
                        # year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number,wbook_xlrd.datemode)
                        # py_date = datetime.datetime(year, month, day, hour, minute, second)

                        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number,
                                                                                      wbook_xlrd.datemode)
                        vfecha = datetime.date(year, month, day)

                        valsrow.append(str(vfecha))
                        # print (vfecha)

                    else:
                        valsrow.append(str(vcell.value))
                        # print (vcell.value)

                # Tengo mi lista de valores en una LISTA
                # Ejemplo ['5585406034.0', '8952034000038976738', '2017-01-23', 'PORTA', '100.0', 'Pendiente']
                # print (valsrow)

                # Recorro mi tupla para tomar los valores y asignarlos
                # newdoc = ArchivoEx(filename=vfilename, docfile=request.FILES['docfile'],numload=vnumload,usuario=vusername)


                for i in range(len(valsrow)):
                    if i == 0:
                        # ent1 = 'DN='  + valsrow[i]
                        vDN = valsrow[i]
                    elif i == 1:
                        # ent2 = 'ICC=' + str(valsrow[i])
                        vICC = valsrow[i]
                    elif i == 2:
                        # ent3 = 'FechaA=' + str(valsrow[i])
                        vFechaA = valsrow[i]
                    elif i == 3:
                        # ent4 = 'Producto=' + str(valsrow[i])
                        vProducto = valsrow[i]
                    elif i == 4:
                        # ent5 = 'Recarga=' + str(valsrow[i])
                        vRecarga = valsrow[i]

                    else:
                        # ent6 = 'Estatus=' + str(valsrow[i])
                        vEstatus = valsrow[i]

                #Calculo la comision
                if vvtaiva == "Sin IVA":
                    if vProducto == "SIM":
                        vComi1  = vRecarga * vporvtasim / 100
                    elif vProducto == "PORTA":
                        vComi1 = vRecarga * vporvtaporta / 100
                    else:
                        vComi1 = vRecarga * vporvta / 100
                # Primero quito el IVA y luego realizo el calculo
                else:
                    vRecsiva = float(vRecarga) / 1.16

                    if vProducto == "SIM":
                        vComi1 = vRecsiva * float(vporvtasim) / 100
                    elif vProducto == "PORTA":
                        vComi1 = vRecsiva * float(vporvtaporta) / 100
                    else:
                        vComi1 = vRecsiva * float(vporvta) / 100

                # Salvo los renglones del Excel, el detalle
                newreg = ArchivoExDet(DN=vDN, ICC=vICC, FechaA=vFechaA, Producto=vProducto, Recarga=vRecarga,
                                      Comision=vComi1, Estatus=vEstatus, filename=vfilename, usuario=vusername)
                newreg.save()

            # Salvo los datos del archivo de excel, el encabezado
            newdoc = ArchivoEx(filename=vfilename, docfile=request.FILES['docfile'], numload=vnumload,
                               prodpor=vlprodpor, usuario=vusername)
            newdoc.save(form)
            # FINALIZO CARGA DEL PRIMER ARCHIVO

            # CARGO EL SEGUNDO ARCHIVO
            # Cargo la primera hora y veo en numero ded renglones
            vsheet = wbook_xlrdprov.sheet_by_index(0)
            nr_rows = vsheet.nrows

            # Comenzamos en el renglon 2, el 1 son los encabezados
            first_row = 2  # nr_rows - 2
            for vrow in range(first_row, nr_rows):
                # print vsheet.row(vrow) #imprime el renglon completo en una tupla con los valores
                valsrow = []  # Preparo mi tupla para ir agregando los valores de c/renglon de excel
                for vcell in vsheet.row(vrow):
                    if vcell.ctype == 3:  # Del tipo 3 son las fechas
                        ms_date_number = vcell.value
                        # manejo de fechas de excel a modelos django-python
                        # year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number,wbook_xlrd.datemode)
                        # py_date = datetime.datetime(year, month, day, hour, minute, second)

                        year, month, day, hour, minute, second = xlrd.xldate_as_tuple(ms_date_number,
                                                                                      wbook_xlrd.datemode)
                        vfecha = datetime.date(year, month, day)

                        valsrow.append(str(vfecha))
                        # print (vfecha)

                    else:
                        valsrow.append(str(vcell.value))
                        # print (vcell.value)

                # Tengo mi lista de valores en una tupla
                # Ejemplo ['5585406034.0', '8952034000038976738', '2017-01-23', 'PORTA', '100.0', 'Pendiente']
                # print (valsrow)

                # Recorro mi tupla para tomar los valores y asignarlos
                # newdoc = ArchivoEx(filename=vfilename, docfile=request.FILES['docfile'],numload=vnumload,usuario=vusername)

                for i in range(len(valsrow)):
                    if i == 0:
                        # ent1 = 'DN='  + valsrow[i]
                        vDN = valsrow[i]
                    elif i == 1:
                        # ent2 = 'ICC=' + str(valsrow[i])
                        vICC = valsrow[i]
                    elif i == 2:
                        # ent3 = 'FechaA=' + str(valsrow[i])
                        vFechaA = valsrow[i]
                    elif i == 3:
                        # ent4 = 'Producto=' + str(valsrow[i])
                        vProducto = valsrow[i]
                    elif i == 4:
                        # ent5 = 'Recarga=' + str(valsrow[i])
                        vRecarga = valsrow[i]
                    elif i == 5:
                        # ent5 = 'Recarga=' + str(valsrow[i])
                        vComision = valsrow[i]
                    else:
                        # ent6 = 'Estatus=' + str(valsrow[i])
                        vEstatus = valsrow[i]
                # Salvo los renglones del Excel, el detalle
                newregprov = ArchivoExDetProv(DN=vDN, ICC=vICC, FechaA=vFechaA, Producto=vProducto, Recarga=vRecarga,
                                              Comision=vComision, Estatus=vEstatus, filename=vfilenameprov,
                                              usuario=vusername)
                newregprov.save()

            # Salvo los datos del archivo de excel, el encabezado
            newdocprov = ArchivoExProv(filename=vfilenameprov, docfile=request.FILES['docfileprov'], numload=vnumload,
                                       usuario=vusername)
            newdocprov.save(form)
            # FINALIZO CARGA DEL SEGUNDO ARCHIVO

            # Ejecuta el el .html defino con la etiqueta en el url
            # url(r'^cargar-excel2/$', 'apps.pvrep.views.upload_file2', name = 'cargar_excel2')
            # Ejecuta proceso upload_file2 y este manda llamar a pvrep/archexcel2.html


            return redirect("/cargar-excel2")

            # return render_to_response('pvrep/archexcel.html', {'form': form}, context_instance=RequestContext(request))

            #Ejecuta directamente pvrep/archexcel2.html y le pasa como parametros todas las variables locales
            #return render_to_response('pvrep/archexcel2.html', locals())

    else:

        form = CargarExcelForm()

    # tambien se puede utilizar render_to_response
    # return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))

    # return render(request, 'pvrep/archexcel.html', {'form': form})

    return render_to_response('pvrep/archexcel.html', {'form': form}, context_instance=RequestContext(request))

    # return render(request,'pvrep/archexcel.html')


# SEGUNDO PROCESO ********************************************************

@login_required()
def upload_file2(request):
    vusuario = request.user

    datexcelenc = ArchivoEx.objects.filter( usuario=vusuario )

    datexcel = ArchivoExDet.objects.filter(usuario=vusuario)

    datexcelprov = ArchivoExDetProv.objects.filter(usuario=vusuario)

    vfilename = ArchivoEx.objects.filter( usuario=vusuario ).get( ).filename
    vfilenameprov = ArchivoExProv.objects.filter(usuario=vusuario).get().filename


    # Tengo los productos y sus % en una STRING = 'GEN' '80' 'SIM' '30' 'PORTA' '20']

    vlprodpor = datexcelenc.get().prodpor

    # Convierto en una lista la informacion del dato de la base que viene en un string

    vlprodpor2 = vlprodpor.split()

    encl = "GEN" in vlprodpor2
    if encl == True:
       indexelem =  vlprodpor2.index("GEN")
       vporgen =  vlprodpor2[indexelem + 1]

    encl = "SIM" in vlprodpor2
    if encl == True:
       indexelem =  vlprodpor2.index("SIM")
       vporsim =  vlprodpor2[indexelem + 1]

    encl = "PORTA" in vlprodpor2
    if encl == True:
       indexelem =  vlprodpor2.index("PORTA")
       vporporta =  vlprodpor2[indexelem + 1]


    # De las pruebas realizadas, si trabajo sobre la instancia datexcel no salva los registros
    # Si trabajo sobre ArchivoExDet.objects...... si salva los registros

    # TRABAJANDO CON EL PRIMER ARCHIVO OPERACIONES LOCALES
    for enc1 in ArchivoExDet.objects.filter(usuario=request.user.id):
        for enc2 in ArchivoExDetProv.objects.filter(DN=enc1.DN):
            enc1.Estatus ="Encontrado"
            enc2.Estatus ="Encontrado"

            newregLP = ArchivoExDetLP (DN=enc1.DN, ICC=enc1.ICC, FechaA=enc1.FechaA, Producto=enc1.Producto,
                                    Recarga=enc1.Recarga, Comision=enc1.Comision,
                                    RecargaProv=enc2.Recarga, ComisionProv=enc2.Comision, Dif=enc2.Comision-enc1.Comision,
                                    Estatus=enc1.Estatus, filename=vfilenameprov, usuario=vusuario)
            newregLP.save ()

            enc2.save()
            enc1.save() # El save debe ir dentro del for, si lo alineo al for sOlo salva el primer registro


    # ArchivoExDet.objects.filter(Estatus='Encontrado').update(Estatus='PUPUPDATE') SI FUNCIONA


    # Cuento el total de registros
    num_reg = ArchivoExDet.objects.count()

    #Realizo operaciones con los que si encontree
    # Me regresa la suma en un diccionario {'vrec_total': Decimal('93440.00')}
    vtotalprod_dic = ArchivoExDet.objects.filter(Estatus='Encontrado').aggregate (vrec_total=Sum ('Recarga'))
    # Tomo el valor total del diccionario que regreso la funcion
    for clave, vtotalprod_rec in vtotalprod_dic.iteritems():
        vtotalprod_rec  #Tengo el total de Recargas de todos los productos

    # Hago lo mismo por PRODUCTO
    # Ventas de PREPAGO  Campo en el modelo(db) Producto = Nombre del producto = PREPAGO, suma la columna de Recarga en db
    vtotal_prep_dic = ArchivoExDet.objects.filter(Producto="PREPAGO", Estatus='Encontrado').aggregate(vsim_total=Sum('Recarga'))

    for clave, vtotal_prep in vtotal_prep_dic.iteritems():
        vtotal_prep #Tengo el total de Recargas de PREPAGO

    # Ventas de PORTA  Campo en el modelo(db) Producto = Nombre del producto = PORTA, suma la columna de Recarga en db
    vtotal_porta_dic = ArchivoExDet.objects.filter(Producto="PORTA", Estatus='Encontrado').aggregate(vsim_total=Sum('Recarga'))

    for clave, vtotal_porta in vtotal_porta_dic.iteritems():
        vtotal_porta #Tengo el total de Recargas de PORTA

    # Ventas de SIM       Campo en el modelo(db) Producto = Nombre del producto = SIM, suma la columna de Recarga en db
    vtotal_sim_dic = ArchivoExDet.objects.filter(Producto="SIM", Estatus='Encontrado').aggregate(vsim_total=Sum('Recarga'))

    for clave, vtotal_sim in vtotal_sim_dic.iteritems():
        vtotal_sim #Tengo el total de Recargas de SIM

    #COMISIONES
    #  Total de comisiones de todos los  Productos  encontrados suma la columna de Comision en db
    vtotcom_dic = ArchivoExDetProv.objects.filter(Estatus='Encontrado').aggregate(vrec_total=Sum('Comision'))

    for clave, vtotalcom in vtotcom_dic.iteritems():
        vtotalcom #Tengo el tital de comisiones


    # comisiones del Producto = Nombre del producto = PREPAGO, suma la columna de Comision en db
    vtotcom_prep_dic = ArchivoExDetProv.objects.filter(Estatus='Encontrado', Producto='PREPAGO').aggregate(vrec_total=Sum('Comision'))

    for clave, vtotalcom_prep in vtotcom_prep_dic.iteritems():
        vtotalcom_prep #Tengo el total de comisiones del Producto =  PREPAGO

    # comisiones del Producto = Nombre del producto = PORTA, suma la columna de Comision en db
    vtotcom_porta_dic = ArchivoExDetProv.objects.filter(Estatus='Encontrado', Producto='PORTA').aggregate(vrec_total=Sum('Comision'))

    for clave, vtotalcom_porta in vtotcom_porta_dic.iteritems():
        vtotalcom_porta #Tengo el total de comisiones del Producto =  PORTA

    # comisiones del Producto = Nombre del producto = SIM, suma la columna de Comision en db
    vtotcom_sim_dic = ArchivoExDetProv.objects.filter(Estatus='Encontrado', Producto='SIM').aggregate(vrec_total=Sum('Comision'))

    for clave, vtotalcom_sim in vtotcom_sim_dic.iteritems():
        vtotalcom_sim #Tengo el total de comisiones del Producto = SIM


    # Contamos los registros del proveedor
    num_regprov = datexcelprov.count()
    # Tomamos las linea encontradas y por lo tanto pagadas.
    datexcelLP  =  ArchivoExDetLP.objects.filter(usuario=vusuario)

    # Tomamos la lineas no encontradas
    for enc1 in ArchivoExDet.objects.filter(usuario=request.user.id, Estatus='Pendiente'):
        newregLNOP = ArchivoExDetLNOP (DN=enc1.DN, ICC=enc1.ICC, FechaA=enc1.FechaA, Producto=enc1.Producto,
                                Recarga=enc1.Recarga, Comision=enc1.Comision,
                                Estatus=enc1.Estatus, filename= vfilename, usuario=vusuario)
        newregLNOP.save ()

    for enc2 in ArchivoExDetProv.objects.filter(usuario=request.user.id, Estatus='No encontrado'):
        newregLNOP = ArchivoExDetLNOP (DN=enc2.DN, ICC=enc2.ICC, FechaA=enc2.FechaA, Producto=enc2.Producto,
                                Recarga=enc2.Recarga, Comision=enc2.Comision,
                                Estatus=enc2.Estatus, filename= vfilenameprov, usuario=vusuario)
        newregLNOP.save ()

    datexcelLNOP = ArchivoExDetLNOP.objects.filter( usuario=vusuario )


    if request.method == 'POST':

        # return render_to_response('pvrep/archexcel2.html', {'form': form}, context_instance=RequestContext(request))
        return render_to_response('pvrep/archexcel2.html', {'datexcel': datexcel, 'datexcelprov': datexcelprov, 'datexcellp':datexcelLP,
                                                            'datexcellnop' : datexcelLNOP, "num_reg": num_reg, "num_regprov": num_regprov,
                                                            "vtotal_prep": vtotal_prep, "vtotal_porta": vtotal_porta,
                                                            "vtotal_sim":vtotal_sim, "vtotalprod_rec":vtotalprod_rec,
                                                            "vtotalcom_prep": vtotalcom_prep, "vtotalcom_porta": vtotalcom_porta,
                                                            "vtotalcom_sim": vtotalcom_sim, "vtotalcom": vtotalcom})

    else:

        # tambien se puede utilizar render_to_response
        # return render_to_response('upload.html', {'form': form}, context_instance = RequestContext(request))

        # return render(request,'pvrep/archexcel.html')
        return render_to_response('pvrep/archexcel2.html', {'datexcel': datexcel, 'datexcelprov': datexcelprov, 'datexcellp':datexcelLP,
                                                            'datexcellnop' : datexcelLNOP, "num_reg": num_reg, "num_regprov": num_regprov,
                                                            "vtotal_prep": vtotal_prep, "vtotal_porta": vtotal_porta,
                                                            "vtotal_sim":vtotal_sim, "vtotalprod_rec":vtotalprod_rec,
                                                            "vtotalcom_prep": vtotalcom_prep, "vtotalcom_porta": vtotalcom_porta,
                                                            "vtotalcom_sim": vtotalcom_sim, "vtotalcom": vtotalcom,
                                                            "vporgen": vporgen, "vporsim": vporsim, "vporporta": vporporta})



