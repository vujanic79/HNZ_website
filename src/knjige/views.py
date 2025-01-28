from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


from .models import Knjiga

@login_required(login_url="/login/")
def knjiga_list_view(request):
	#list out objects
	qs = Knjiga.objects.all()
	template_name = 'list.html'
	context = {'object_list': qs}
	return render(request, template_name, context)


@login_required(login_url="/login/")
def knjiga_detail_view(request,slug):
	#one object -> detail view
	obj = get_object_or_404(Knjiga, slug=slug)
	template_name = "detail.html"
	context = {"object": obj}
	return render(request, template_name, context)