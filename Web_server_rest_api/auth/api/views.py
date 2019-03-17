from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
import json
import requests
import datetime, secrets
from auth.models import Organisation, User, AccidentLocation
from math import pi,sqrt,sin,cos,atan2
from django.utils import timezone
import json
import requests


def locationToKm(lat1, long1, lat2, long2):
    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_long = (long2 - long1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = 6367 * c
    #mi = 3956 * c
    return km


def sendLocation(request):
    newAccidentLocation = AccidentLocation()
    newAccidentLocation.id = secrets.token_hex(8)
    newAccidentLocation.latitude = request.POST.get('latitude', None)
    newAccidentLocation.longitude = request.POST.get('longitude', None)
    print(newAccidentLocation.latitude)
    print(newAccidentLocation.longitude)
    newAccidentLocation.timestamp = datetime.datetime.now(tz=timezone.utc)

    organisations = Organisation.objects.all()
    vicinityOrgs = ""
    for org in organisations:
        dist = locationToKm(float(newAccidentLocation.latitude), float(newAccidentLocation.longitude), float(org.latitude), float(org.longitude))
        if dist <= 2:
            vicinityOrgs += org.id + ","
            r = sendMsg(org.mobile)


    minDist = locationToKm(float(newAccidentLocation.latitude), float(newAccidentLocation.longitude), float(organisations[0].latitude), float(organisations[0].longitude))
    minId = organisations[0].id
    if vicinityOrgs == "":
        for org in organisations:
            dist = locationToKm(float(newAccidentLocation.latitude), float(newAccidentLocation.longitude), float(org.latitude), float(org.longitude))
            if dist < minDist:
                minDist = dist
                minId = org.id

        newAccidentLocation.orgs = minId
        minOrg = Organisation.objects.filter(id=minId)

        r = sendMsg(minOrg[0].mobile)
    else:
        newAccidentLocation.orgs = vicinityOrgs


    newAccidentLocation.save()
    return HttpResponse("Successfull")

def sendBlackSpotData(request):
    organisations = Organisation.objects.all()
    organisationCount = len(organisations)
    accidents = AccidentLocation.objects.all()
    accidentCount = len(accidents)

    locations = []
    for accident in accidents:
        obj = {
            'lat': float(accident.latitude),
            'lng': float(accident.longitude),
        }
        locations.append(obj)

    context = {
        'locations': json.dumps(locations),
    }
    return HttpResponse(context)


def sendMsg(to):
    url = "https://smsapi.engineeringtgr.com/send/?Mobile=8329720183&Password=abhi@123&Message=Please Check your accident log on portal. A new accident has been reported in your vicinity.&To=" + to + "&Key=kotka9R7BAc8CHTaw1SVZOmz6otPv"
    r = requests.post(url)
    print(r.content)
    return HttpResponse(r.content)



