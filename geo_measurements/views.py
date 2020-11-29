from django.shortcuts import render,get_object_or_404
from .models import GeoMeasureMent
from .forms import MeasurementModelForm
from geopy.geocoders import Nominatim
from .utils import get_geo_ip,get_center_coordinates,get_proper_distance
from geopy.distance import geodesic
import folium

def calculate_distance_view(request):
    distance = None
    destination = None
    obj = get_object_or_404(GeoMeasureMent,id=1)
    form = MeasurementModelForm(request.POST or None)
    geo_locator = Nominatim(user_agent='geo_measurements')
    ip_addr = '43.224.108.173'
    country,city,lat,lon = get_geo_ip(ip_addr)
    location = geo_locator.geocode(city)
    
    # location coordinates
    l_lat = lat
    l_lon = lon
    point_a = (l_lat,l_lon)

    # initial folium map
    map_folium = folium.Map(width=800,height=500,location=get_center_coordinates(l_lat,l_lon))
    # add folium marker in map (location)
    folium.Marker([l_lat,l_lon],tooltip='Click here for more',popup=city['city'],
                        icon=folium.Icon(color='red')).add_to(map_folium)



    if form.is_valid():
        instance = form.save(commit=False)
        destination_input = form.cleaned_data.get('destination')
        destination = geo_locator.geocode(destination_input)

        # destination coordinates
        des_lat = destination.latitude
        des_lon = destination.longitude
        point_b = (des_lat,des_lon)

        # distance calculation
        distance = round(geodesic(point_a,point_b).km,2)
        
        # folium map modification
        map_folium = folium.Map(width=800,height=500,
                            location=get_center_coordinates(l_lat,l_lon,des_lat,des_lon),
                            zoom_start=get_proper_distance(distance))
        # add folium marker in map (location)
        folium.Marker([l_lat,l_lon],tooltip='Click here for more',popup=city['city'],
                        icon=folium.Icon(color='red')).add_to(map_folium)
        # add folium marker in map (destination)
        folium.Marker([des_lat,des_lon],tooltip='Click here for more',popup=destination,
                        icon=folium.Icon(color='blue',icon='cloud')).add_to(map_folium)

        # draw the line beetween location and destination
        line = folium.PolyLine(locations=[point_a,point_b],weight=2,color='red')
        map_folium.add_child(line)

        instance.location = location
        instance.distance = distance
        instance.save()
    map_folium = map_folium._repr_html_()

    context = {
        'distance':distance,
        'form' : form,
        'destination': destination,
        'map' : map_folium,
    }
    return render(request,'geo_measurement/main.html',context)
