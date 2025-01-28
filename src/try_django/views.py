from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from .forms import ContactForm
from blog.models import SluzbaPost
from django.contrib.auth.decorators import login_required

@login_required(login_url="/login/")
def home_page(request):
	my_title = "hello there..."
	qs = SluzbaPost.objects.all()[:5]
	context = {"title": "Welcome to try Django", "blog_list": qs}
	return render(request, "home.html", context)

@login_required(login_url="/login/")
def about_page(request):
	return render(request, "about.html", {"title": "About us"})

@login_required(login_url="/login/")
def contact_page(request):
	form = ContactForm(request.POST or None)
	if form.is_valid():
		print(form.cleaned_data)
		form = ContactForm()
	context = {
		"title": "Kontakt informacije", "form": form
	}
	return render(request, "form.html", context)

@login_required(login_url="/login/")
def example_page(request):
	context 		= {"title": "Example"}
	template_name 	= "hello_world.html"
	templete_obj 	= get_template(template_name)
	rendered_item	= templete_obj.render(context)
	return HttpResponse(rendered_item)  
