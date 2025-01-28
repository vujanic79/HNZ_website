from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect


# Create your views here.

from .models import SluzbaPost, PojanjaPost, Folder,FolderSluzbe
from .forms import SluzbaPostModelForm

@login_required(login_url="/login/")
def sluzba_post_list_view(request,slug):
	#list out objects
	if slug:
		folder = FolderSluzbe.objects.get(slug=slug)
		qs = SluzbaPost.objects.filter(folder=folder)
		print(f"Filtered by folder: {folder.name}, Songs: {qs}")
	print(folder)
	template_name = 'blog/list.html'
	context = {'sluzba_list': qs, 'folder': folder if slug else None}
	for obj in qs:
		print(f"Naslov: {obj.title}, Tema: {obj.tema}, Audio: {obj.audio}")
	return render(request, template_name, context)

@login_required(login_url="/login/")
def pojanja_list_view(request,slug):
	if slug:
		folder = Folder.objects.get(slug=slug)
		qs = PojanjaPost.objects.filter(folder=folder)
		print(f"Filtered by folder: {folder.name}, Songs: {qs}")
	print(folder)
	template_name = 'blog/list-pojanja.html'
	context = {'object_list': qs, 'folder': folder if slug else None}
	return render(request, template_name, context)

@login_required(login_url="/login/")
def folder_list(request):
	folders = Folder.objects.all().order_by('name')
	return render(request, 'blog/folders.html', {'folders': folders})

	
@login_required(login_url="/login/")
def folder_list_sluzbe(request):
	folders = FolderSluzbe.objects.all().order_by('name')
	return render(request, 'blog/folders-sluzbe.html', {'folders': folders})


#@login_required
@staff_member_required
def blog_post_create_view(request):
	#create objects
	form = SluzbaPostModelForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.user = request.user
		obj.save()
		form = SluzbaPostModelForm()
	template_name = 'form.html'
	context = {'form': form}
	return render(request, template_name, context)

@staff_member_required
def blog_post_detail_view(request,slug):
	#one object -> detail view
	obj = get_object_or_404(SluzbaPost, slug=slug)
	template_name = "blog/detail.html"
	context = {"object": obj}
	return render(request, template_name, context)

@staff_member_required
def blog_post_update_view(request,slug):
	obj = get_object_or_404(SluzbaPost, slug=slug)
	form = SluzbaPostModelForm(request.POST or None, request.FILES or None, instance=obj)
	if form.is_valid():
		form.save()
	template_name = "form.html"
	context = {"form": form, "title": f"Update {obj.title}"}
	return render(request, template_name, context)

@staff_member_required
def blog_post_delete_view(request,slug):

	obj = get_object_or_404(SluzbaPost, slug=slug)
	template_name = "blog/delete.html"
	if request.method == "POST":
		obj.delete()
		return redirect("/blog")
	context = {"object": obj,'form': ''}
	return render(request, template_name, context)