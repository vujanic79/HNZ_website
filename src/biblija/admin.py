from django.contrib import admin

# Register your models here.

from .models import StariZavetKnjige, StariZavetGlave, StariZavetText, NoviZavetKnjige, NoviZavetGlave, NoviZavetText

admin.site.register(StariZavetKnjige)
admin.site.register(StariZavetGlave)
admin.site.register(StariZavetText)
admin.site.register(NoviZavetKnjige)
admin.site.register(NoviZavetGlave)
admin.site.register(NoviZavetText)
