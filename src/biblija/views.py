from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect
import re 

from .models import StariZavetKnjige, StariZavetGlave, StariZavetText, NoviZavetKnjige, NoviZavetGlave, NoviZavetText


@login_required(login_url="/login/")
def stari_zavet_list(request):
	folders = StariZavetKnjige.objects.all()
	return render(request, 'stari-zavet.html', {'folders': folders})

	
@login_required(login_url="/login/")
def stari_zavet_list_view(request,knjiga_slug):
	knjiga = get_object_or_404(StariZavetKnjige, slug=knjiga_slug)
	glave = knjiga.glave.all().order_by('name')
	return render(request, 'stari-zavet-glave.html', {'knjiga': knjiga,'glave': glave})

@login_required(login_url="/login/")
def stari_zavet_text_view(request, knjiga_slug, glava_slug):
    glava = get_object_or_404(StariZavetGlave, knjiga__slug=knjiga_slug, slug=glava_slug)
    knjiga = get_object_or_404(StariZavetKnjige, slug=knjiga_slug)
    text = StariZavetText.objects.filter(glava=glava)  # Filter by ForeignKey field
    for t in text:
        t.content = t.content.replace('\n', '<br>')
    return render(request, 'stari-zavet-text.html', {'glava': glava, 'text': text,'knjiga': knjiga})



@login_required(login_url="/login/")
def novi_zavet_list(request):
	folders = NoviZavetKnjige.objects.all()
	return render(request, 'novi-zavet.html', {'folders': folders})

	
@login_required(login_url="/login/")
def novi_zavet_list_view(request,knjiga_slug):
	knjiga = get_object_or_404(NoviZavetKnjige, slug=knjiga_slug)
	glave = knjiga.glave.all().order_by('name')
	return render(request, 'novi-zavet-glave.html', {'knjiga': knjiga,'glave': glave})

@login_required(login_url="/login/")
def novi_zavet_text_view(request, knjiga_slug, glava_slug):
    glava = get_object_or_404(NoviZavetGlave, knjiga__slug=knjiga_slug, slug=glava_slug)
    knjiga = get_object_or_404(NoviZavetKnjige, slug=knjiga_slug)
    text = NoviZavetText.objects.filter(glava=glava)  # Filter by ForeignKey field
    for t in text:
        t.content = t.content.replace('\n', '<br>')
    return render(request, 'novi-zavet-text.html', {'glava': glava, 'text': text,'knjiga': knjiga})