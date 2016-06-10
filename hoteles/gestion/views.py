# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect

import urllib2
from datetime import datetime

from django.template.loader import get_template, render_to_string
from django.shortcuts import render, render_to_response
from django.template import Context
from django.template.response import TemplateResponse

from django.views.decorators.csrf import csrf_exempt

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from models import hoteles, imagenes, comentarios, selecciones, usuarios

from xml.sax import make_parser
from xml.sax.handler import ContentHandler

########### Clases ########### 

class HotelHandler(ContentHandler):
    def __init__(self):

        self.inContent = False
        self.theContent = ''

        self.hotel = ''
        self.num_id = 0
        self.name = ''
        self.email = ''
        self.phone = ''
        self.body = ''
        self.web = ''
        self.address = ''
        self.incategoria = False
        self.categoria = ''
        self.insubcategoria = False
        self.estrellas = ''

        self.url = []


    # Call when an element starts
    def startElement(self, tag, attributes):

        if tag == 'service':
            self.num_id = attributes.getValue(attributes.getNames()[1])
        elif tag == 'name':
            self.inContent = True
        elif tag == 'email':
            self.inContent = True
        elif tag == 'phone':
            self.inContent = True
        elif tag == 'body':
            self.inContent = True
        elif tag == 'web':
            self.inContent = True
        elif tag == 'address':
            self.inContent = True
        elif tag == 'url':
            self.inContent = True
        elif tag == 'item':
            atributo = attributes.getValue(attributes.getNames()[0])
            if atributo == 'Categoria':
                self.inContent = True
                self.incategoria = True
            elif atributo == 'SubCategoria':
                self.inContent = True
                self.insubcategoria = True

    # Call when an elements ends
    def endElement(self, tag):

        if tag == 'name':
            self.name = self.theContent
        elif tag == 'email':
            self.email = self.theContent
        elif tag == 'phone':
            self.phone = self.theContent
        elif tag == 'body':
            self.body = self.theContent
        elif tag == 'web':
            self.web = self.theContent
        elif tag == 'address':
            self.address = self.theContent
        elif tag == 'url':
            self.url.append(self.theContent)
        elif tag == 'item':
            if self.incategoria == True:
                self.categoria = self.theContent
                self.incategoria = False
            elif self.insubcategoria == True:
                self.estrellas = self.theContent
                self.insubcategoria = False
        elif tag == 'service':

            try:
                hotel = hoteles.objects.get(num_id=self.num_id)

                if hotel.name != self.name:
                    hotel.name = self.name
                    hotel.save()
                if hotel.email != self.email:
                    hotel.email = self.email
                    hotel.save()
                if hotel.phone != self.phone:
                    hotel.phone = self.phone
                    hotel.save()
                if hotel.description != self.body:
                    hotel.description = self.body
                    hotel.save()
                if hotel.web != self.web:
                    hotel.web = self.web
                    hotel.save()
                if hotel.address != self.address:
                    hotel.address = self.address
                    hotel.save()
                if hotel.categoria != self.categoria:
                    hotel.categoria = self.categoria
                    hotel.save()
                if hotel.estrellas != self.estrellas:
                    hotel.estrellas = self.estrellas
                    hotel.save()

            except hoteles.DoesNotExist:
                hotel = hoteles(num_id=self.num_id,
                                name=self.name,
                                email=self.email,
                                phone=self.phone,
                                description=self.body,
                                web=self.web,
                                address=self.address,
                                categoria=self.categoria,
                                estrellas=self.estrellas)
                hotel.save()

            self.hotel = hotel

            for count in range(0, len(self.url)):
                try:
                    imagen = imagenes.objects.get(enlace=self.url[count])

                    if imagen.hotel != self.hotel:
                        imagen.hotel = self.hotel
                        imagen.save()

                except imagenes.DoesNotExist:
                    imagen = imagenes(enlace=self.url[count], hotel=self.hotel)
                    imagen.save()

            self.url = []
                        
        if self.inContent:
            self.inContent = False
            self.theContent = ''   
      
    # Call when a character is read
    def characters(self, chars):
        if self.inContent:
            self.theContent = self.theContent + chars

########### Funciones ########### 

# Esta es la main page ----------------------------------------------------------------------

@csrf_exempt
def inicio(request):
    template = get_template('main_template.html')

    if request.user.is_authenticated():
        login_box = '<form id="login" action="http://127.0.0.1:8000/logout" method="POST">' +\
                    '<table>' +\
                    '<tr>' +\
                    '<td>User: </td>' +\
                    '<td>' + str(request.user) + '</td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td><input type="submit" value="logout"></td>' +\
                    '</tr>' +\
                    '</table>' +\
                    '</form>'         
    else: 
        login_box = '<form id="login" action="http://127.0.0.1:8000/login" method="POST">' +\
                    '<table>' +\
                    '<tr>' +\
                    '<td>User</td>' +\
                    '<td><input type="text" name="username"></td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td>Password</td>' +\
                    '<td><input type="password" name="password"></td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td><input type="submit" value="Login"></td>' +\
                    '</tr>' +\
                    '</table>' +\
                    '</form>'

    hotels_list = hoteles.objects.all()
    the_hotels = []
    num_comments = []
    the_mosts_comment = []

    if len(hotels_list) != 0:

        for hotel in hotels_list:
            comentario = comentarios.objects.filter(hotel=hotel)
            num_comments.append(len(comentario))
            the_hotels.append(hotel)

        for x in range(0, 9):
            indx = num_comments[max(num_comments)]
            hotel = the_hotels[indx]
            the_mosts_comment.append(hotel)
            num_comments.remove(num_comments[indx])
            the_hotels.remove(the_hotels[indx])

        hotel_data = ''

        for count in range(0, len(the_mosts_comment)):
            imagen = imagenes.objects.filter(hotel=the_mosts_comment[count])
            hotel_data +=   '<div id="element">' +\
                            '<img src="' + imagen[0].enlace + '" width="100%">' +\
                            '<h2>' + the_mosts_comment[count].name + '</h2>' +\
                            '<p>Direccion: ' + the_mosts_comment[count].address + '</p>' +\
                            '<p><a href="http://127.0.0.1:8000/alojamientos/' +\
                            str(the_mosts_comment[count].num_id) + '">Mas informacion</a></p>' +\
                            '</div>'

        seleccion = selecciones.objects.all()
        users = usuarios.objects.all()

        if len(seleccion) != 0:
            all_selections = ''

            for user in users:
                user_all_selections = selecciones.objects.filter(usuario=user)

                if len(user_all_selections) != 0:
                    all_selections += '<h2><a href="http://127.0.0.1:8000/' +\
                                      user_all_selections[0].usuario.nombre +\
                                      '">' +\
                                      user_all_selections[0].usuario.titulo_selecciones +\
                                      '</a></h2>'
        else:
            all_selections = '<h2>No existen selecciones de usuarios</h2>'

        try:
            CSS_file = open('templates/' + str(request.user) + '.css', 'r')
            styles_source = 'http://127.0.0.1:8000/templates/' + str(request.user) + '.css'
            CSS_file.close()
        except:
            styles_source = 'http://127.0.0.1:8000/templates/styles.css'

        context = ({'login_box': login_box,
                    'hotel_data': hotel_data,
                    'all_selections': all_selections,
                    'styles_source': styles_source})
        
        return HttpResponse(template.render(context))
    else:
        return HttpResponseRedirect('http://127.0.0.1:8000/refresh')


#---------------------------------------------------------------------------------------------
# Esta es mi funcion para hacer login --------------------------------------------------------

@csrf_exempt
def login_view(request):

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(username=username, password=password)

    if user is not None:

        if user.is_active:

            login(request, user)

            return HttpResponseRedirect('http://127.0.0.1:8000/')

        else:
            # Devuelve un 'disabled account' error
            return HttpResponse('Tu cuenta ha sido baneada')
    else:
        # Devuleve un 'invalid login' error 
        return HttpResponseRedirect('http://127.0.0.1:8000/')

#---------------------------------------------------------------------------------------------
# Esta es mi funcion para hacer logout -------------------------------------------------------

@csrf_exempt
def logout_view(request):

    logout(request)

    return HttpResponseRedirect('http://127.0.0.1:8000')

#---------------------------------------------------------------------------------------------
# Esta es la pagina about, que explica el funcionamiento de la practica ----------------------

def about(request):

    template = get_template('about.html')
    context = ({})

    return HttpResponse(template.render(context))

#---------------------------------------------------------------------------------------------
# Uso esta funcion refresh para actualizar las bases de datos --------------------------------

def refresh(request):

    XML_es = urllib2.urlopen('http://www.esmadrid.com/opendata/alojamientos_es.xml')

    XML_file = open('templates/XML_es.xml', 'w')
    XML_file.write(XML_es.read())
    XML_file.close()

    XML_file = open('templates/XML_es.xml', 'r')


    XML_parser = make_parser()
    XML_handler = HotelHandler()
    XML_parser.setContentHandler(XML_handler)

    XML_parser.parse(XML_file)

    XML_file.close()

    return HttpResponseRedirect('http://127.0.0.1:8000/')

#---------------------------------------------------------------------------------------------
# Esta funcion es para mostrar la lista con todos los alojamientos ---------------------------

@csrf_exempt
def alojamientos(request):

    template = get_template('main_template.html')

    if request.method == 'GET':
        hotel = hoteles.objects.all()
    else:
        try:
            categoria = request.POST['categoria']
            hotel = hoteles.objects.filter(categoria=categoria)
        except:
            estrellas = request.POST['estrellas']
            hotel = hoteles.objects.filter(estrellas=estrellas)

    hotel_data =    '<div id="element">' +\
                    '<form action="http://127.0.0.1:8000/alojamientos" method="POST">' +\
                    '<p>Busqueda por categoria</p>' +\
                    '<select name="categoria">' +\
                    '<option value="Hoteles" selected="selected">Hoteles</option>' +\
                    '<option value="Hostales">Hostales</option>' +\
                    '<option value="Albergues">Albergues</option>' +\
                    '</select>' +\
                    '<input type="submit" value="Buscar">' +\
                    '</form>' +\
                    '<form action="http://127.0.0.1:8000/alojamientos" method="POST">' +\
                    '<p>Busqueda por estrellas</p>' +\
                    '<select name="estrellas">' +\
                    '<option value="1 estrella" selected="selected">1 estrella</option>' +\
                    '<option value="2 estrellas">2 estrellas</option>' +\
                    '<option value="3 estrellas">3 estrellas</option>' +\
                    '<option value="4 estrellas">4 estrellas</option>' +\
                    '<input type="submit" value="Buscar">' +\
                    '</select>' +\
                    '</form>' +\
                    '</div>'

    for count in range(0, len(hotel)):

        hotel_data += '<div id="element">' +\
                      '<h2>' + hotel[count].name + '</h2>' +\
                      '<a href="http://127.0.0.1:8000/alojamientos/' +\
                      str(hotel[count].num_id) +\
                      '">Mas informacion</a>' +\
                      '</div>'

    if request.user.is_authenticated():

        login_box ='<form id="login" action="http://127.0.0.1:8000/logout" method="POST">' +\
                    '<table>' +\
                    '<tr>' +\
                    '<td>User: </td>' +\
                    '<td>' + str(request.user) + '</td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td><input type="submit" value="logout"></td>' +\
                    '</tr>' +\
                    '</table>' +\
                    '</form>'         
   
    else:
        
        login_box ='<form id="login" action="http://127.0.0.1:8000/login" method="POST">' +\
                    '<table>' +\
                    '<tr>' +\
                    '<td>User</td>' +\
                    '<td><input type="text" name="username"></td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td>Password</td>' +\
                    '<td><input type="password" name="password"></td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td><input type="submit" value="Login"></td>' +\
                    '</tr>' +\
                    '</table>' +\
                    '</form>'

    seleccion = selecciones.objects.all()
    users = usuarios.objects.all()

    if len(seleccion) != 0:
        all_selections = ''

        for user in users:
            user_all_selections = selecciones.objects.filter(usuario=user)

            if len(user_all_selections) != 0:
                all_selections += '<h2><a href="http://127.0.0.1:8000/' +\
                                  user_all_selections[0].usuario.nombre +\
                                  '">' +\
                                  user_all_selections[0].usuario.titulo_selecciones +\
                                  '</a></h2>'
    else:
        all_selections = '<h2>No existen selecciones de usuarios</h2>'

    try:
        CSS_file = open('templates/' + str(request.user) + '.css', 'r')
        styles_source = 'http://127.0.0.1:8000/templates/' + str(request.user) + '.css'
        CSS_file.close()
    except:
        styles_source = 'http://127.0.0.1:8000/templates/styles.css'

    context = ({'login_box': login_box,
                'hotel_data': hotel_data,
                'all_selections': all_selections,
                'styles_source': styles_source})
      
    return HttpResponse(template.render(context))

#---------------------------------------------------------------------------------------------
# Esta funcion es para mostrar los detalles de un solo alojamiento ---------------------------

@csrf_exempt
def alojamientos_id(request, num_id):
    template = get_template('main_template.html')
    allowed = True

    try:
        hotel = hoteles.objects.get(num_id=num_id)
        imagen = imagenes.objects.filter(hotel=hotel)

        if request.method == 'POST':

            try:
                comentario = comentarios.objects.get(hotel=hotel, usuario=request.user)
                allowed = False
            except:
                comentario = comentarios(comentario=request.POST['comentario'], hotel=hotel, usuario=request.user)
                comentario.save()

        comentario = comentarios.objects.filter(hotel=hotel)
        hotel_data =    '<div id="element">' +\
                        '<h2>' + hotel.name + '</h2>' +\
                        '<p>Email: <a href=' + hotel.email + '>' + hotel.email + '</a></p>' +\
                        '<p>Telefono: ' + hotel.phone + '</p>' +\
                        '<p>Descripcion: ' + hotel.description + '</p>' +\
                        '<p>Web: <a href=' + hotel.web + '>' + hotel.web + '</a></p>' +\
                        '<p>Direccion: ' + hotel.address + '</p>'

        for count in range(0, len(imagen)):
            hotel_data += '<img src="' + imagen[count].enlace + '" width="100%">'

        hotel_data += '</div>'

        for count in range(0, len(comentario)):
            hotel_data +=   '<div id="element">' +\
                            '<p>Comentario de ' + comentario[count].usuario + '</p>' +\
                            '<p>' + comentario[count].comentario + '</p>' +\
                            '</div>'        

        if request.user.is_authenticated():
            login_box ='<form id="login" action="http://127.0.0.1:8000/logout" method="POST">' +\
                        '<table>' +\
                        '<tr>' +\
                        '<td>User: </td>' +\
                        '<td>' + str(request.user) + '</td>' +\
                        '</tr>' +\
                        '<tr>' +\
                        '<td><input type="submit" value="logout"></td>' +\
                        '</tr>' +\
                        '</table>' +\
                        '</form>'

            if allowed:
                hotel_data += '<form action="http://127.0.0.1:8000/' + str(request.user)  +\
                              '" method="POST">' +\
                              '<input type="submit" value="Agregar a mi seleccion">' +\
                              '</form>' +\
                              '<form action="http://127.0.0.1:8000/alojamientos/' + str(num_id) +\
                              '" method="POST">' +\
                              '<p>Comente el sitio </p>' +\
                              '<textarea name="comentario" rows"60" cols="60">' +\
                              '</textarea>' +\
                              '<input type="submit" value="Enviar">' +\
                              '</form>'
            else:
                hotel_data += '<p>No se le permiten mas comentarios</p>'
       
        else:
            login_box = '<form id="login" action="http://127.0.0.1:8000/login" method="POST">' +\
                        '<table>' +\
                        '<tr>' +\
                        '<td>User</td>' +\
                        '<td><input type="text" name="username"></td>' +\
                        '</tr>' +\
                        '<tr>' +\
                        '<td>Password</td>' +\
                        '<td><input type="password" name="password"></td>' +\
                        '</tr>' +\
                        '<tr>' +\
                        '<td><input type="submit" value="Login"></td>' +\
                        '</tr>' +\
                        '</table>' +\
                        '</form>'
            
        seleccion = selecciones.objects.all()
        users = usuarios.objects.all()

        if len(seleccion) != 0:
            all_selections = ''

            for user in users:
                user_all_selections = selecciones.objects.filter(usuario=user)

                if len(user_all_selections) != 0:
                    all_selections += '<h2><a href="http://127.0.0.1:8000/' +\
                                      user_all_selections[0].usuario.nombre +\
                                      '">' +\
                                      user_all_selections[0].usuario.titulo_selecciones +\
                                      '</a></h2>'
        else:
            all_selections = '<h2>No existen selecciones de usuarios</h2>'

        try:
            CSS_file = open('templates/' + str(request.user) + '.css', 'r')
            styles_source = 'http://127.0.0.1:8000/templates/' + str(request.user) + '.css'
            CSS_file.close()
        except:
            styles_source = 'http://127.0.0.1:8000/templates/styles.css'

        context = ({'login_box': login_box,
                    'hotel_data': hotel_data,
                    'all_selections': all_selections,
                    'styles_source': styles_source})
        
    except hoteles.DoesNotExist:
        return HttpResponse('Ha ocurrido un error inesperado en el servidor')

    return HttpResponse(template.render(context))

#---------------------------------------------------------------------------------------------
# Esta funcion es la pagina personal de cada usuario -----------------------------------------

@csrf_exempt
def usuario(request, user):
    template = get_template('main_template.html')
    styles_source = '"http://127.0.0.1:8000/templates/styles.css"'

    if request.method == 'POST':

        if request.user.is_authenticated() and str(request.user) == user:

            try:
                usuario = usuarios.objects.get(nombre=user)
            except usuarios.DoesNotExist:
                usuario = usuarios(nombre=user, titulo_selecciones='Pagina del usuario ' + user)
                usuario.save()

            URL = request.META['HTTP_REFERER']
            URL = URL.split('/')

            if URL[-1] == user:
                body = request.body
                body = body.split('=')

                if body[0] == 'colour':
                    colour = body[1] 

                    try:
                        CSS_file = open('templates/' + user + '.css', 'r')
                        styles = CSS_file.read()
                        CSS_file.close()                      
                    except:
                        styles = render_to_string('styles.css')

                    styles = styles.replace('#666666', colour)
                    styles = styles.replace('gray', colour)
                    styles = styles.replace('white', colour)
                    styles = styles.replace('red', colour)
                    styles = styles.replace('blue', colour)
                    CSS_file = open('templates/' + user + '.css', 'w')
                    CSS_file.write(styles)
                    CSS_file.close()
                    styles_source = '"http://127.0.0.1:8000/templates/' + user + '.css"'
                elif body[0] == 'size':
                    size = body[1]

                    try:
                        CSS_file = open('templates/' + user + '.css', 'r')
                        styles = CSS_file.read()
                        CSS_file.close()
                    except:
                        styles = render_to_string('styles.css')

                    styles = styles.replace('font-size: 14px', 'font-size: ' + size)
                    styles = styles.replace('font-size: 10px', 'font-size: ' + size)
                    styles = styles.replace('font-size: 18px', 'font-size: ' + size)
                    CSS_file = open('templates/' + user + '.css', 'w')
                    CSS_file.write(styles)
                    CSS_file.close()
                    styles_source = '"http://127.0.0.1:8000/templates/' + user + '.css"'
                elif body[0] == 'new_name':
                    new_name = body[1]
                    new_name = new_name.replace('+',' ')
                    usuario.titulo_selecciones = new_name
                    usuario.save()
                else:
                    return HttpResponse('Ha ocurrido un error inesperado en el servidor')

            else:   
                num_id = URL[-1]

                try:
                    hotel = hoteles.objects.get(num_id=num_id)
                    ahora = datetime.now()
                    seleccion = selecciones(usuario=usuario, hotel=hotel, fecha=ahora)
                    seleccion.save()
                except:
                    return HttpResponse('Ha ocurrido un error inesperado en el servidor')
           
        else:
            return HttpResponse('ACCESS DENIED --- Para modificar tu cuenta primero tienes que loguearte')
           
    try:
        usuario = usuarios.objects.get(nombre=user)
        seleccion = selecciones.objects.filter(usuario=usuario)
    except:
        return HttpResponse('Ha ocurrido un error inesperado en el servidor')

    if request.user.is_authenticated() and str(request.user) == user:
        hotel_data ='<div id="element">' +\
                    '<form action="http://127.0.0.1:8000/' + user + '" method="POST">' +\
                    '<p>Aqui puede cambiar el nombre de su seleccion </p>' +\
                    '<input type="text" name="new_name">' +\
                    '</textarea>' +\
                    '<input type="submit" value="Enviar">' +\
                    '</form>' +\
                    '</div>' +\
                    '<div id="element">' +\
                    '<form action="http://127.0.0.1:8000/' + user + '" method="POST">' +\
                    '<p>Aqui puede cambiar las dimensiones de las letras</p>' +\
                    '<select name="size">' +\
                    '<option value="14px" selected="selected">100%</option>' +\
                    '<option value="10px">75%</option>' +\
                    '<option value="18px">125%</option>' +\
                    '</select>' +\
                    '<input type="submit" value="Cambiar">' +\
                    '</form>' +\
                    '<form action="http://127.0.0.1:8000/' + user + '" method="POST">' +\
                    '<p>Aqui puede cambiar el color de fondo</p>' +\
                    '<select name="colour">' +\
                    '<option value="gray" selected="selected">Default</option>' +\
                    '<option value="white">Blanco</option>' +\
                    '<option value="red">Rojo</option>' +\
                    '<option value="blue">Azul</option>' +\
                    '<input type="submit" value="Cambiar">' +\
                    '</select>' +\
                    '</form>' +\
                    '</div>'
    else:
        hotel_data = ''

    for count in range(0, len(seleccion)):

        imagen = imagenes.objects.filter(hotel=seleccion[count].hotel)

        hotel_data +=   '<div id="element">' +\
                        '<img src="' + imagen[0].enlace + '" width="100%">' +\
                        '<h2>' + seleccion[count].hotel.name + '</h2>' +\
                        '<p>Direccion: ' + seleccion[count].hotel.address + '</p>' +\
                        '<p><a href="http://127.0.0.1:8000/alojamientos/' + str(seleccion[count].hotel.num_id) + '">Mas informacion</a></p>' +\
                        '<p>Fecha de seleccion: ' + str(seleccion[count].fecha) + '</p>' +\
                        '</div>'

    if request.user.is_authenticated():
        login_box ='<form id="login" action="http://127.0.0.1:8000/logout" method="POST">' +\
                    '<table>' +\
                    '<tr>' +\
                    '<td>User: </td>' +\
                    '<td>' + str(request.user) + '</td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td><input type="submit" value="logout"></td>' +\
                    '</tr>' +\
                    '</table>' +\
                    '</form>'     
    else:
        login_box ='<form id="login" action="http://127.0.0.1:8000/login" method="POST">' +\
                    '<table>' +\
                    '<tr>' +\
                    '<td>User</td>' +\
                    '<td><input type="text" name="username"></td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td>Password</td>' +\
                    '<td><input type="password" name="password"></td>' +\
                    '</tr>' +\
                    '<tr>' +\
                    '<td><input type="submit" value="Login"></td>' +\
                    '</tr>' +\
                    '</table>' +\
                    '</form>'

    seleccion = selecciones.objects.all()
    users = usuarios.objects.all()

    if len(seleccion) != 0:
        all_selections = ''

        for user in users:
            user_all_selections = selecciones.objects.filter(usuario=user)

            if len(user_all_selections) != 0:
                all_selections += '<h2><a href="http://127.0.0.1:8000/' +\
                                  user_all_selections[0].usuario.nombre +\
                                  '">' +\
                                  user_all_selections[0].usuario.titulo_selecciones +\
                                  '</a></h2>'
    else:
        all_selections = '<h2>No existen selecciones de usuarios</h2>'

    try:
        CSS_file = open('templates/' + str(request.user) + '.css', 'r')
        styles_source = 'http://127.0.0.1:8000/templates/' + str(request.user) + '.css'
        CSS_file.close()
    except:
        styles_source = 'http://127.0.0.1:8000/templates/styles.css'

    context = ({'login_box': login_box,
                'hotel_data': hotel_data,
                'all_selections': all_selections,
                'styles_source': styles_source})

    return HttpResponse(template.render(context))


#---------------------------------------------------------------------------------------------
































