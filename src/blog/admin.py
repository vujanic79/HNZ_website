from django.contrib import admin

# Register your models here.


from .models import SluzbaPost, PojanjaPost, Folder, FolderSluzbe

admin.site.register(SluzbaPost)
admin.site.register(PojanjaPost)
admin.site.register(Folder)
admin.site.register(FolderSluzbe)