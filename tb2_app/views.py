from django.shortcuts import render, redirect
from django.contrib import messages
from tb2_app.models import User, Trip
import bcrypt

def login_and_registration(request):
    if 'id' in request.session:
        return redirect('/dashboard')
    return render(request, 'login_registration.html')

def register(request):
    errors = User.objects.validate_user(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        hash_pass = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        user = User.objects.create(first_name=first_name, last_name=last_name, password=hash_pass, email=email)
        request.session['id'] = user.id
        request.session.save()
        return redirect('/dashboard')

def login(request):
    try:
        user = User.objects.get(email=request.POST['email'])
    except:
        messages.error(request, 'Not a valid email address')
        return redirect('/')
    if bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        request.session['id'] = user.id
        request.session.save()
        return redirect('/dashboard')
    else:
        messages.error(request, 'Incorrect password')
        return redirect('/')

def dashboard(request):
    if not 'id' in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    user_trips = Trip.objects.filter(created_by=user).order_by('start_date')
    other_trips = Trip.objects.exclude(created_by=user).order_by('start_date')
    for trip in user.trips_joined.all():
        other_trips = other_trips.exclude(id=trip.id)
    joined_trips = user.trips_joined.all()
    context = {
        'user': user,
        'user_trips': user_trips,
        'joined_trips': joined_trips,
        'other_trips': other_trips,
    }
    return render(request, 'dashboard.html', context)

def new_trip(request):
    if 'id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user
    }
    return render(request, 'new_trip.html', context)

def create_trip(request):
    if 'id' not in request.session:
        return redirect('/')
    
    errors = Trip.objects.validate_trip(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        destination = request.POST['destination']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']
        plan = request.POST['plan']
        user = User.objects.get(id=request.session['id'])
        Trip.objects.create(destination=destination, start_date=start_date, end_date=end_date, plan=plan, created_by=user)
        return redirect('/dashboard')

def edit_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    if trip.created_by.id != request.session['id']:
        return redirect('/dashboard')
    user = User.objects.get(id=request.session['id'])
    context = {
        'user': user,
        'trip': trip
    }
    return render(request, 'edit_trip.html', context)

def update_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    if trip.created_by.id != request.session['id']:
        return redirect('/dashboard')
    errors = Trip.objects.validate_trip(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f'/trips/edit/{trip_id}')
    else:
        trip.destination = request.POST['destination']
        trip.start_date = request.POST['start_date']
        trip.end_date = request.POST['end_date']
        trip.plan = request.POST['plan']
        trip.save()
        return redirect('/dashboard')

    return redirect('/dashboard')

def delete_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    if trip.created_by.id != request.session['id']:
        return redirect('/')
    trip.delete()
    return redirect('/dashboard')

def trip_details(request, trip_id):
    if 'id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['id'])
    travelers = trip.travelers.order_by('first_name', 'last_name').all()
    context = {
        'user': user,
        'trip': trip,
        'travelers': travelers
    }
    return render(request, 'trip_details.html', context)

def join_trip(request, trip_id):
    if 'id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['id'])
    if user.id != trip.created_by.id:
        trip.travelers.add(user)
    return redirect('/dashboard')

def cancel_join(request, trip_id):
    if 'id' not in request.session:
        return redirect('/')
    trip = Trip.objects.get(id=trip_id)
    user = User.objects.get(id=request.session['id'])
    trip.travelers.remove(user)
    return redirect('/dashboard')

def logout(request):
    request.session.clear()
    return redirect('/')