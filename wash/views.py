from django.db.models import Count
from user.models import User
from django.shortcuts import render

from .models import Order, CarType, WashType, Car


# Create your views here.
def home(request):
    return render(request, "carwashs/home.html")

def washers(request):
     return render(request=request, template_name='carwashs/washers.html', context={
            'washers': User.objects.filter(status=User.Status.washer.value).annotate(washed_count=Count('orders'))
        })


def history(request):
    return render(request, "carwashs/history.html")


def contact(request):
    return render(request, "carwashs/contact.html")