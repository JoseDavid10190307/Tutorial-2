from django.db import models

class Vuelo(models.Model):
    id_vuelo = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100)
    price = models.IntegerField()
