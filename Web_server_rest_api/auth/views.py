import json
from math import pi, sqrt, sin, cos, atan2
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from .forms import UserForm
from .models import User, Organisation, AccidentLocation
import hashlib, secrets

def register(request):
    if request.method == 'POST':
        newUser = User()
        newUser.name = request.POST['name']
        newUser.email = request.POST['email']
        password = request.POST['password']
        sha = hashlib.sha256()
        sha.update(password.encode('utf-8'))
        password_hash = sha.hexdigest()
        newUser.password_hash = password_hash

        newUser.save()
        request.session['email'] = newUser.email
        request.session['name'] = newUser.name
        return render(request, 'profile.html', {'user': newUser})
    return render(request, 'register.html')


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        sha = hashlib.sha256()
        sha.update(password.encode('utf-8'))
        password_hash = sha.hexdigest()

        user = User.objects.filter(email=email, password_hash=password_hash) or None

        if user is None:
            return render(request, 'login.html')
        else:
            request.session['email'] = user[0].email
            request.session['name'] = user[0].name

            myOrg = Organisation.objects.filter(email=email) or None


            organisations = Organisation.objects.all()
            organisationCount = len(organisations)
            accidents = AccidentLocation.objects.all()
            accidentCount = len(accidents)
            vicinityAcc = []

            for accident in accidents:
                print(accident.orgs)
                if accident.orgs.count(',') >= 1:
                    temp = accident.orgs.split(",")
                    for t in temp:
                        if t == myOrg[0].id:
                            vicinityAcc.append(accident)
                else:
                    if accident.orgs == myOrg[0].id:
                        vicinityAcc.append(accident)

            vicinityAccCount = len(vicinityAcc)

            context = {
                'user': user[0],
                'organisationCount': organisationCount,
                'accidentCount': accidentCount,
                'accidents': accidents,
                'vicinityAcc': vicinityAcc,
                'vicinityAccCount': vicinityAccCount
            }
            return render (request, 'dashboard.html', context)

    return render(request, 'login.html')


def profile(request):
    if request.method == "POST":
        newOrganisation = Organisation()
        newOrganisation.id = secrets.token_hex(8)
        newOrganisation.email = request.POST['email']
        newOrganisation.mobile = request.POST['mobile']
        newOrganisation.latitude = request.POST['latitude']
        newOrganisation.longitude = request.POST['longitude']
        newOrganisation.address = request.POST['address']
        newOrganisation.city = request.POST['city']
        newOrganisation.state = request.POST['state']
        newOrganisation.postal_code = request.POST['postal_code']
        newOrganisation.type = request.POST['type']
        newOrganisation.about = request.POST['about']

        newOrganisation.save()
        user = User.objects.filter(email=newOrganisation.email)

        email = request.session['email']
        myOrg = Organisation.objects.filter(email=email) or None

        organisations = Organisation.objects.all()
        organisationCount = len(organisations)
        accidents = AccidentLocation.objects.all()
        accidentCount = len(accidents)
        vicinityAcc = []

        for accident in accidents:
            print(accident.orgs)
            if accident.orgs.count(',') >= 1:
                temp = accident.orgs.split(",")
                for t in temp:
                    if t == myOrg[0].id:
                        vicinityAcc.append(accident)
            else:
                if accident.orgs == myOrg[0].id:
                    vicinityAcc.append(accident)

        vicinityAccCount = len(vicinityAcc)

        context = {
            'user': user[0],
            'organisationCount': organisationCount,
            'accidentCount': accidentCount,
            'accidents': accidents,
            'vicinityAcc': vicinityAcc,
            'vicinityAccCount': vicinityAccCount
        }
        return render(request, 'dashboard.html', context)

    return render(request, 'profile.html')


def dashboard(request):
    if request.session['email'] is not None:
        email = request.session['email']
        user = User.objects.filter(email=email)

        email = request.session['email']
        myOrg = Organisation.objects.filter(email=email) or None

        organisations = Organisation.objects.all()
        organisationCount = len(organisations)
        accidents = AccidentLocation.objects.all()
        accidentCount = len(accidents)
        vicinityAcc = []

        for accident in accidents:
            print(accident.orgs)
            if accident.orgs.count(',') >= 1:
                temp = accident.orgs.split(",")
                for t in temp:
                    if t == myOrg[0].id:
                        vicinityAcc.append(accident)
            else:
                if accident.orgs == myOrg[0].id:
                    vicinityAcc.append(accident)

        vicinityAccCount = len(vicinityAcc)

        context = {
            'user': user,
            'organisationCount': organisationCount,
            'accidentCount': accidentCount,
            'accidents': accidents,
            'vicinityAcc': vicinityAcc,
            'vicinityAccCount': vicinityAccCount
        }

        return render(request, 'dashboard.html', context)
    else:
        return render(request, 'login.html')


def blackSpot(request):
    email = request.session['email']
    user = User.objects.filter(email=email)

    email = request.session['email']
    myOrg = Organisation.objects.filter(email=email) or None

    organisations = Organisation.objects.all()
    organisationCount = len(organisations)
    accidents = AccidentLocation.objects.all()
    accidentCount = len(accidents)
    vicinityAcc = []

    for accident in accidents:
        print(accident.orgs)
        if accident.orgs.count(',') >= 1:
            temp = accident.orgs.split(",")
            for t in temp:
                if t == myOrg[0].id:
                    vicinityAcc.append(accident)
        else:
            if accident.orgs == myOrg[0].id:
                vicinityAcc.append(accident)

    vicinityAccCount = len(vicinityAcc)

    locations = []
    for accident in accidents:
        obj = {
            'lat': float(accident.latitude),
            'lng': float(accident.longitude),
        }
        locations.append(obj)

    context = {
        'user': user[0],
        'organisationCount': organisationCount,
        'accidentCount': accidentCount,
        'accidents': accidents,
        'locations': json.dumps(locations),
        'vicinityAccCount': vicinityAccCount
    }
    return render(request, 'maps.html', context)


def logout(request):
    request.session['email'] = None
    request.session['name'] = None
    return render(request, 'login.html')



def locationToKm(lat1, long1, lat2, long2):
    degree_to_rad = float(pi / 180.0)

    d_lat = (lat2 - lat1) * degree_to_rad
    d_long = (long2 - long1) * degree_to_rad

    a = pow(sin(d_lat / 2), 2) + cos(lat1 * degree_to_rad) * cos(lat2 * degree_to_rad) * pow(sin(d_long / 2), 2)
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    km = 6367 * c
    # mi = 3956 * c
    return km


def detectBlackspot(clusters):
    clusterCount = [0] * len(clusters)
    blackspot = [False] * len(clusters)
    blackSpotThreshhold = 5
    i = 0
    for cluster in clusters:
        clusterCount[i] = len(cluster)
        if clusterCount[i] >= blackSpotThreshhold:
            blackspot[i] = True
        else:
            blackspot[i] = False
        i += 1

    print(clusterCount)
    print(blackspot)


p = [(19.0760, 72.8777), (18.9220, 72.8347), (18.9217, 72.8330), (19.1095, 72.8241), (18.9398, 72.8354),
     (18.9230, 72.8367), (18.9199, 72.8378), (18.9198, 72.8376)]
clusters = []

while len(p) is not 0:
    tempCluster = []
    tempCluster.append(p[0])
    p.remove(p[0])

    flag = 0
    i = 0
    j = len(p)
    while (i < j):
        print(i)
        for pc in tempCluster:
            dist = locationToKm(p[i][0], p[i][1], pc[0], pc[1])
            print(p[i][0], p[i][1], pc[0], pc[1], dist)
            if dist <= 1:
                tempCluster.append(p[i])
                p.remove(p[i])
                # print("removed", p[i])
                i = i - 1
                break
        i += 1
        j = len(p)

    clusters.append(tempCluster)

print(clusters)
detectBlackspot(clusters)

















