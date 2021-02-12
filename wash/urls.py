from django.urls import path
from . import views

app_name = 'wash'

urlpatterns = [
    path("", views.home, name="home"),
    path("washers/", views.washers, name="washers"),
    path("history/", views.history, name="history"),
    path('home/', views.home, name="home"),
    path('cars/', views.cars, name="cars"),
    path('washers/<int:pk>/', views.washer_detail, name='washer-detail'),

]
