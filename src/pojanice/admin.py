from django.contrib import admin

# Register your models here.

from .models import ListaPojanja, Pojanje, Pojanica, StaraPojanicaFolder, StaraPojanica


admin.site.register(Pojanica)
admin.site.register(ListaPojanja)
admin.site.register(Pojanje)
admin.site.register(StaraPojanicaFolder)
admin.site.register(StaraPojanica)