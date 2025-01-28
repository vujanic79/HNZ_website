from django.shortcuts import render
from blog.models import SluzbaPost, PojanjaPost
from pojanice.models import Pojanje
from knjige.models import Knjiga
from biblija.models import StariZavetText, NoviZavetText
from django.contrib.auth.decorators import login_required
# Create your views here.
from .models import SearchQuery
from django.utils.safestring import mark_safe
import re

@login_required(login_url="/login/")
def search_view(request):
	query = request.GET.get('q', None)
	user = None
	if request.user.is_authenticated:
		user = request.user
	context = {"query":query}
	if query is not None:
		SearchQuery.objects.create(user=user,query=query)
		sluzba_list = SluzbaPost.objects.search(query=query)
		context['sluzba_list'] = sluzba_list
	return render(request,'searches/view.html',context)


@login_required(login_url="/login/")
def search_pojanje_view(request):
	query = request.GET.get('q', None)
	user = None
	if request.user.is_authenticated:
		user = request.user
	context = {"query":query}
	if query is not None:
		SearchQuery.objects.create(user=user,query=query)
		pojanja_list = PojanjaPost.objects.search(query=query)
		context['pojanja_list'] = pojanja_list
	return render(request,'searches/view-pojanja.html',context)

@login_required(login_url="/login/")
def search_knjige_view(request):
	query = request.GET.get('q', None)
	user = None
	if request.user.is_authenticated:
		user = request.user
	context = {"query":query}
	if query is not None:
		SearchQuery.objects.create(user=user,query=query)
		knjiga_list = Knjiga.objects.search(query=query)
		context['knjiga_list'] = knjiga_list
	return render(request,'searches/view-knjiga.html',context)

@login_required(login_url="/login/")
def search_pojanice_view(request):
	query = request.GET.get('q', None)
	user = None
	if request.user.is_authenticated:
		user = request.user
	context = {"query":query}
	if query is not None:
		SearchQuery.objects.create(user=user,query=query)
		pojanice_list = Pojanje.objects.search(query=query)
		context['pojanice_list'] = pojanice_list
		print(pojanice_list)
	return render(request,'searches/view-pojanice.html',context)


@login_required(login_url="/login/")
def search_stari_view(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user

    context = {"query": query}
    if query is not None:
        # Save the search query if the user is logged in
        SearchQuery.objects.create(user=user, query=query)
        
        # Filter texts containing the search query
        stari_list = StariZavetText.objects.search(query=query)

        # Prepare context to include verses matching the query
        verses_with_query = []
        for text_obj in stari_list:
            # Split content into verses assuming each verse is separated by a newline or period
            verses = re.split(r'\n|\.', text_obj.content)

            for verse in verses:
                # Check if the query is in the verse
                if query.lower() in verse.lower():
                    # Highlight the search term in the verse
                    highlighted_verse = re.sub(f'({query})', r'<mark>\1</mark>', verse, flags=re.IGNORECASE)
                    
                    # Create a custom dictionary for the verse and related data
                    verse_data = {
                        'knjiga_name': text_obj.glava.knjiga.name,
                        'glava_number': text_obj.glava.name,
                        'verse_content': mark_safe(highlighted_verse),  # Use mark_safe to render HTML safely
                        'knjiga_slug': text_obj.glava.knjiga.slug,  # Add the slug of the book
                        'glava_slug': text_obj.glava.slug,  # Add the slug of the chapter
                    }
                    
                    verses_with_query.append(verse_data)
        
        # Pass the filtered verses to the context
        context['verses_with_query'] = verses_with_query

    return render(request, 'searches/stari-view.html', context)

@login_required(login_url="/login/")
def search_novi_view(request):
    query = request.GET.get('q', None)
    user = None
    if request.user.is_authenticated:
        user = request.user

    context = {"query": query}
    if query is not None:
        # Save the search query if the user is logged in
        SearchQuery.objects.create(user=user, query=query)
        
        # Filter texts containing the search query
        stari_list = NoviZavetText.objects.search(query=query)

        # Prepare context to include verses matching the query
        verses_with_query = []
        for text_obj in stari_list:
            # Split content into verses assuming each verse is separated by a newline or period
            verses = re.split(r'\n|\.', text_obj.content)

            for verse in verses:
                # Check if the query is in the verse
                if query.lower() in verse.lower():
                    # Highlight the search term in the verse
                    highlighted_verse = re.sub(f'({query})', r'<mark>\1</mark>', verse, flags=re.IGNORECASE)
                    
                    # Create a custom dictionary for the verse and related data
                    verse_data = {
                        'knjiga_name': text_obj.glava.knjiga.name,
                        'glava_number': text_obj.glava.name,
                        'verse_content': mark_safe(highlighted_verse),  # Use mark_safe to render HTML safely
                        'knjiga_slug': text_obj.glava.knjiga.slug,  # Add the slug of the book
                        'glava_slug': text_obj.glava.slug,  # Add the slug of the chapter
                    }
                    
                    verses_with_query.append(verse_data)
        
        # Pass the filtered verses to the context
        context['verses_with_query'] = verses_with_query

    return render(request, 'searches/novi-view.html', context)