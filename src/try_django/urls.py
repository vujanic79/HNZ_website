"""try_django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('sluzba/', include('sluzba.urls'))
"""
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.contrib import admin
from django.urls import path, re_path, include

from biblija.views import(
    stari_zavet_list,
    stari_zavet_text_view,
    stari_zavet_list_view,
    novi_zavet_list,
    novi_zavet_text_view,
    novi_zavet_list_view,
    )

from knjige.views import(
    knjiga_list_view,
    knjiga_detail_view,
    )

from pojanice.views import(
    pojanice_list,
    pojanica_list_view,
    pojanja_text_view,
    stare_pojanja_text_view,
    stare_pojanice_list,
    )

from blog.views import (
    sluzba_post_list_view,
    pojanja_list_view,
    folder_list,
    folder_list_sluzbe,
    )

from searches.views import( 
    search_view,
    search_pojanje_view,
    search_knjige_view,
    search_pojanice_view,
    search_stari_view,
    search_novi_view,
    )

from .views import (
    home_page, 
    about_page, 
    contact_page,
    example_page
)

from mape.views import (
    map_view,
    )
urlpatterns = [
    path('', about_page),
    path('mapa-skupstina/', map_view,name='map_view'),
    path('stare-pojanice/', stare_pojanice_list,name='stare_pojanice_list'),
    path('stare-pojanice/<str:pojanica_slug>/', stare_pojanja_text_view,name='stare_pojanja_text_view'),
    path('nove-pojanice/', pojanice_list,name='pojanice_list'),
    path('nove-pojanice/<str:pojanica_slug>/', pojanica_list_view,name='pojanica_list_view'),
    path('nove-pojanice/<slug:pojanica_slug>/<slug:pojanje_slug>/', pojanja_text_view, name='pojanja_text_view'),
    path('stari-zavet/', stari_zavet_list,name='stari_zavet_list'),
    path('knjige-i-spisi/<str:slug>/', knjiga_detail_view,name='knjiga_detail_view'),
    path('knjige-i-spisi/', knjiga_list_view,name='knjiga_list_view'),
    path('stari-zavet/<str:knjiga_slug>/', stari_zavet_list_view,name='stari_zavet_list_view'),
    path('stari-zavet/<slug:knjiga_slug>/<slug:glava_slug>/', stari_zavet_text_view, name='stari_zavet_text_view'),
    path('novi-zavet/', novi_zavet_list,name='novi_zavet_list'),
    path('novi-zavet/<str:knjiga_slug>/', novi_zavet_list_view,name='novi_zavet_list_view'),
    path('novi-zavet/<slug:knjiga_slug>/<slug:glava_slug>/', novi_zavet_text_view, name='novi_zavet_text_view'),
    path('novi-zavet/', about_page),
    path('sluzbe/',folder_list_sluzbe,name='folder_list_sluzbe'),
    path('sluzbe/<str:slug>/',sluzba_post_list_view,name='sluzba_post_list_view'),
    path('pojanja/',folder_list,name='folder_list'),
    path('pojanja/<str:slug>/', pojanja_list_view, name='pojanja_list_view'),
    path('search/',search_view,name='search'),
    path('search/novi-zavet/',search_novi_view,name='search_novi_view'),
    path('search/stari-zavet/',search_stari_view,name='search_stari_view'),
    path('search/pojanja/',search_pojanje_view),
    path('search/knjige-i-spisi/',search_knjige_view,name='search_knjige_view'),
    path('search/nove-pojanice/',search_pojanice_view,name='search_pojanice_view'),
    path('kontakt/', contact_page),
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
