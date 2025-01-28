from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
import re 

from .models import ListaPojanja, Pojanje, Pojanica, StaraPojanica, StaraPojanicaFolder


@login_required(login_url="/login/")
def pojanice_list(request):
	folders = Pojanica.objects.all()
	return render(request, 'pojanica.html', {'folders': folders})

	
@login_required(login_url="/login/")
def pojanica_list_view(request,pojanica_slug):
	lista = get_object_or_404(Pojanica, slug=pojanica_slug)
	pojanja = lista.pojanica.all().order_by('broj')
	return render(request, 'lista-pojanja.html', {'lista': lista,'pojanja': pojanja})

@login_required(login_url="/login/")
def pojanja_text_view(request, pojanica_slug, pojanje_slug):
    pojanica = get_object_or_404(Pojanica, slug=pojanica_slug)
    pojanje = get_object_or_404(ListaPojanja, folder=pojanica, slug=pojanje_slug)
    text = Pojanje.objects.filter(pojanje=pojanje)

    return render(request, 'pojanje-text.html', {'pojanje': pojanje, 'text': text, 'pojanica': pojanica})

@login_required(login_url="/login/")
def stare_pojanice_list(request):
	folders = StaraPojanicaFolder.objects.all()
	return render(request, 'stare-pojanice.html', {'folders': folders})


@login_required(login_url="/login/")
def stare_pojanja_text_view(request, pojanica_slug):
    pojanica = get_object_or_404(StaraPojanicaFolder, slug=pojanica_slug)
    text = StaraPojanica.objects.filter(pojanje=pojanica)  
    pdf_file = text.first().file.url if text.exists() and text.first().file else None
    return render(request, 'stare-pojanice-text.html', {'pdf_file':pdf_file,'text': text,'pojanica': pojanica})
