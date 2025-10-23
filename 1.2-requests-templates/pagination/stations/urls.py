from django.urls import path
from stations import views

urlpatterns = [
    path('', views.index, name='index'),
    path('stations/', views.bus_stations, name='bus_stations'),
]