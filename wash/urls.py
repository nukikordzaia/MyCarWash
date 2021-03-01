from django.urls import path
from . import views
from wash.views import WashersView, CarsView, WasherDetailView

app_name = 'wash'

urlpatterns = [
    path("", views.home, name="home"),
    path("washers/", WashersView.as_view(), name="washers"),
    path("history/", views.history, name="history"),
    path('home/', views.home, name="home"),
    path('cars/', CarsView.as_view(), name="cars"),
    # path('cars/', CarListView.as_view()),
    path('washers/<int:pk>/', WasherDetailView.as_view(), name='washer-detail'),

]
