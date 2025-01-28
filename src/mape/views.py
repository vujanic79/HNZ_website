from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Mesto
import folium
import branca
import folium.plugins as plugins

@login_required(login_url="/login/")
def map_view(request):
    mesta = Mesto.objects.all()  # Query the Mesto model
    m = folium.Map(location=[45.410346, 20.160774], zoom_start=9)
    markers = []
    feature_group = folium.FeatureGroup(name="Mesta")

    # Prepare a list of places to pass to the template
    for mesto in mesta:
        koordinate = (mesto.lat, mesto.lon)
        # Determine the marker color based on status
        if mesto.status == "Aktivna":
            prodata = False
            color = 'green'
        elif mesto.status == "Petrovaradin":
            prodata = False
            color = 'blue'
            print(mesto.status)
        elif mesto.status == "Budisava":
            prodata = False
            color = 'darkblue'
        elif mesto.status == "Neaktivna":
            prodata = False
            color = 'lightgray'
        else:
            prodata = True
            color = 'black'

        
        if mesto.fotografija and hasattr(mesto.fotografija, 'url'):
            image_url = request.build_absolute_uri(mesto.fotografija.url)
            image_html = f'<img src="{image_url}" style="width: 100%; height: auto; max-width: 250px; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);" alt="{mesto.mesto} Image">'
        else:
            image_html = '<div style="width: 100%; max-width: 250px; height: 150px; display: flex; align-items: center; justify-content: center; background-color: #f0f0f0; border-radius: 10px; box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.2);">Fotografija ne postoji</div>'
        
        html = f"""
        <div style="display: flex; flex-direction: row; align-items: flex-start; width: 100%; max-width: 600px; flex-wrap: wrap;">
            <div style="flex: 1; padding: 10px; width: 100%; max-width: 50%; box-sizing: border-box;">
                <h2 style="font-size: 1.5em; margin-bottom: 10px;">{mesto.mesto}</h2>
                <p><strong>Adresa:</strong> {mesto.adresa if mesto.adresa else '/'}</p>
                <p><strong>Status:</strong> {mesto.status if mesto.status else 'Ne postoji'}</p>
                <p><strong>Istorija:</strong> {mesto.opis}</p>
            </div>
            <div style="flex: 1; padding: 10px; max-width: 50%; width: 100%; box-sizing: border-box; display: flex; justify-content: center;">
                {image_html}
            </div>
        </div>
        """

        # Create the IFrame and add the popup to the marker
        iframe = branca.element.IFrame(html=html, width=600, height=350)
        popup = folium.Popup(iframe, max_width=650)

        # Add marker to the FeatureGroup with the name to search for
        marker = folium.Marker(
            location=koordinate,
            popup=popup,
            icon=folium.Icon(color=color),
            name=mesto.mesto  # This is crucial for the Search plugin
        )
        feature_group.add_child(marker)  # Add marker to the FeatureGroup
        markers.append(mesto.mesto)  # Collect mesto names for the search

    # Add the FeatureGroup to the map
    feature_group.add_to(m)

    # Create a search plugin
    search = plugins.Search(
        layer=feature_group,  # Use the FeatureGroup for the search
        search_label='name',  # Use 'name' as this matches the attribute set in the markers
        placeholder='Search for mesto...',
        collapsed=False,
        search=markers,  # This contains the list of mesto names
        zoom_to=True,  # Automatically zoom to the marker when found
    )
    search.add_to(m)  # Add the search to the map after all markers are added

    # Create the map container
    map_container = branca.element.Figure(height="100%")
    map_container.add_child(m)

    context = {
        'mapa': map_container._repr_html_(),
        'places': mesta  # Pass the list of dictionaries to the context
    }

    return render(request, 'mape.html', context)
