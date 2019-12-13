from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_and_registration),
    path('register', views.register),
    path('login', views.login),
    path('dashboard', views.dashboard),
    path('trips/new', views.new_trip),
    path('trips/edit/<int:trip_id>', views.edit_trip),
    path('trips/update/<int:trip_id>', views.update_trip),
    path('trips/destroy/<int:trip_id>', views.delete_trip),
    path('trips/<int:trip_id>', views.trip_details),
    path('trips/join/<int:trip_id>', views.join_trip),
    path('trips/cancel/<int:trip_id>', views.cancel_join),
    path('create_trip', views.create_trip),
    path('logout', views.logout),
]
