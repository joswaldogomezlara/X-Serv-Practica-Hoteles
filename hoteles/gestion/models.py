from __future__ import unicode_literals

from django.db import models

# Create your models here.
    
class hoteles(models.Model):
    num_id = models.IntegerField(null=True)
    name = models.CharField(max_length=64)
    email = models.CharField(max_length=64)
    phone = models.CharField(max_length=64)
    description = models.TextField()
    web = models.CharField(max_length=64)
    address = models.CharField(max_length=64)
    categoria = models.CharField(max_length=64, null=True)
    estrellas = models.CharField(max_length=64, null=True)

class comentarios(models.Model):
    comentario = models.TextField()
    hotel = models.ForeignKey(hoteles)
    usuario = models.CharField(max_length=64, null=True)

class imagenes(models.Model):
    enlace = models.CharField(max_length=64)
    hotel = models.ForeignKey(hoteles)

class usuarios(models.Model):
    nombre = models.CharField(max_length=64, null=True)
    titulo_selecciones = models.CharField(max_length=64, null=True)

class selecciones(models.Model):
    usuario = models.ForeignKey(usuarios, null=True)
    hotel = models.ForeignKey(hoteles)
    fecha = models.DateTimeField(null=True)

