from datetime import datetime
from wash.models import Car
from django.utils import timezone
from decimal import Decimal
from typing import Dict, Optional
from django.core.handlers.wsgi import WSGIRequest
from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count, Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from user.models import User
from wash.forms import CarForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.
def home(request):
    return render(request, "carwashs/home.html")


def history(request):
    return render(request, "carwashs/history.html")


def washers(request: WSGIRequest) -> HttpResponse:
    washer_q = Q()
    q = request.GET.get('q')
    print(q)
    if q:
        washer_q &= Q(first_name__icontains=q) | Q(last_name__icontains=q)
    context = {
        'washers': User.objects.filter(status=User.Status.washer.value).filter(washer_q).annotate(
            washed_count=Count('orders')),
        # **order_info
    }
    return render(request=request, template_name='carwashs/washers.html', context=context)


def cars(request):
    car_list = Car.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(car_list, 8)
    try:
        cars = paginator.page(page)
    except PageNotAnInteger:
        cars = paginator.page(1)
    except EmptyPage:
        cars = paginator.page(paginator.num_pages)

    car_form = CarForm()
    if request.method == 'POST':
        print(request.POST)
        car_form = CarForm(request.POST)
        if car_form.is_valid():
            car_form.save()

    context = {
        'cars': cars,
        'car_form': car_form,
    }
    return render(request=request, template_name='carwashs/cars.html', context=context)




def washer_detail(request: WSGIRequest, pk: int) -> HttpResponse:
    washer: User = get_object_or_404(
        User.objects.filter(status=User.Status.washer.value),
        pk=pk
    )
    earned_money_q = ExpressionWrapper(
        F('price') * F('employee__salary') / Decimal('100.0'),
        output_field=DecimalField()
    )
    now = timezone.now()
    washer_salary_info: Dict[str, Optional[Decimal]] = washer.orders.filter(end_date__isnull=False) \
        .annotate(earned_per_order=earned_money_q) \
        .aggregate(
        earned_money_year=Sum(
            'earned_per_order',
            filter=Q(end_date__gte=now - timezone.timedelta(days=365))
        ),
        washed_last_year=Count(
            'id',
            filter=Q(end_date__gte=now - timezone.timedelta(days=365))
        ),
        earned_money_month=Sum(
            'earned_per_order',
            filter=Q(end_date__gte=now - timezone.timedelta(weeks=4))
        ),
        washed_last_month=Count(
            'id',
            filter=Q(end_date__gte=now - timezone.timedelta(weeks=4))
        ),
        earned_money_week=Sum(
            'earned_per_order',
            filter=Q(end_date__gte=now - timezone.timedelta(days=7))
        ),
        washed_last_week=Count(
            'id',
            filter=Q(end_date__gte=now - timezone.timedelta(days=7))
        )
    )
    return render(request, template_name='carwashs/washer-detail.html', context={
        'washer': washer,
        **washer_salary_info
    })