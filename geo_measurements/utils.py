from django.contrib.gis.geoip2 import GeoIP2

def get_geo_ip(ip):
    geo_ip = GeoIP2()
    country = geo_ip.country(ip)
    city = geo_ip.city(ip)
    lat,lon = geo_ip.lat_lon(ip)
    return country,city,lat,lon

def get_center_coordinates(latA,lonA,latB=None,lonB=None):
    cord = (latA,lonA)
    if latB:
        cord = [(latA+latB)/2,(lonA+lonB)/2]
    return cord

def get_proper_distance(distance):
    if distance <=100:
        return 8
    elif distance > 100 and distance < 5000:
        return 4 
    else:
        return 2
        
