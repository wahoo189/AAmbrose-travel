from django.shortcuts import render, redirect
from django.contrib import messages
from . import models
from datetime import datetime

# Create your views here.
def index(request):
    print models.Users.objects.all().values('username')
    if 'user_id' not in request.session:
        request.session['user_id'] = ''
    if 'page' not in request.session:
        request.session['page'] = ''
    context = {
        'page' : request.session['page']
    }
    print request.session['page']
    return render(request, 'travel_app/index.html', context)

def login(request):
    current_user = models.Users.objects.filter(username = request.POST['user_login'])
    request.session['page'] = 'login'
    if not current_user:
        messages.add_message(request, messages.INFO, 'Username is not valid')
        return redirect('/')
    if current_user[0].password != request.POST['pass_login']:
        messages.add_message(request, messages.INFO, 'Incorrect Password')
        return redirect('/')
    request.session['user_id'] = current_user[0].id
    return redirect('/travels')

def register(request):
    user_check = models.Users.objects.filter(username = request.POST['username'])
    request.session['page'] = 'register'
    if len(request.POST['name']) < 3 or len(request.POST['username']) < 3:
        messages.add_message(request, messages.INFO, 'Name and Username must be at least 3 characters')
        print "Not so fast"
        return redirect('/')
    if user_check:
        messages.add_message(request, messages.INFO, 'That username is already taken')
        return redirect('/')
    if len(request.POST['pass_init']) < 8:
        messages.add_message(request, messages.INFO, 'Please make password at least 8 characters')
        return redirect('/')
    if request.POST['pass_init'] != request.POST['pass_confirm']:
        messages.add_message(request, messages.INFO, 'Password and Confirmation must match')
        return redirect('/')
    models.Users.objects.create(name = request.POST['name'], username = request.POST['username'], password = request.POST['pass_init'])
    return redirect('/')

def home(request):
    print "Session ID", request.session['user_id']
    user = models.Users.objects.get(id = request.session['user_id'])
    myTrips = models.Trips.objects.filter(user_id = user)
    joinTrips = models.Joins.objects.filter(user_id = user)
    otherTrips = models.Trips.objects.exclude(user_id = models.Users.objects.get(id = request.session['user_id'])).exclude(joins__in = models.Joins.objects.filter(user_id = request.session['user_id']))
    context = {
        'user' : user,
        'trips' : myTrips,
        'others' : otherTrips,
        'joins' : joinTrips
    }
    return render(request, 'travel_app/home.html', context)

def add(request):
    return render(request, 'travel_app/add.html')

def create(request):
    nowStr = datetime.now().strftime('%Y-%m-%d')
    print nowStr
    if not request.POST['destination'] or not request.POST['description'] or not request.POST['travel_start'] or not request.POST['travel_end']:
        messages.add_message(request, messages.INFO, 'Please complete all fields')
        return redirect('/travels/add')
    print request.POST['travel_start']
    if nowStr >= request.POST['travel_start']:
        messages.add_message(request, messages.INFO, 'Start date must not be in the past')
        return redirect('/travels/add')
    if request.POST['travel_start'] > request.POST['travel_end']:
        messages.add_message(request, messages.INFO, 'Travel Date To must be after Travel Date From')
        return redirect('/travels/add')
    models.Trips.objects.create(user_id = models.Users.objects.get(id=request.session['user_id']), destination = request.POST['destination'], plan = request.POST['description'], travel_start = request.POST['travel_start'], travel_end = request.POST['travel_end'])
    return redirect('/travels')

def trip(request,id):
    trip = models.Trips.objects.get(id=id)
    joins = models.Joins.objects.filter(trip_id = trip)
    context = {
        'trip' : trip,
        'joins' : joins
    }
    return render(request, 'travel_app/trip.html', context)

def join(request,id):
    models.Joins.objects.create(user_id = models.Users.objects.get(id=request.session['user_id']), trip_id = models.Trips.objects.get(id = id))
    return redirect('/travels')

def logout(request):
    del request.session['user_id']
    return redirect('/')
