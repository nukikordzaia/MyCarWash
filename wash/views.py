from datetime import datetime
from decimal import Decimal
from typing import Dict, Optional

from django.db.models import F, Sum, ExpressionWrapper, DecimalField, Count, Q
from django.shortcuts import render, redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin

from user.models import User
from wash.forms import CarForm, OrderForm
from wash.models import Car, Order


# Create your views here.
def home(request):
    return render(request, "carwashs/home.html")


def history(request):
    return render(request, "carwashs/history.html")


class WashersView(ListView):
    template_name = 'carwashs/washers.html'

    def get_queryset(self):
        washer_q = Q()
        q = self.request.GET.get('q')
        if q:
            washer_q &= Q(first_name__icontains=q) | Q(last_name__icontains=q)
        return User.objects.filter(washer_q, status=User.Status.washer.value).annotate(
            washed_count=Count('orders')
        )


class CarsView(ListView):
    template_name = 'carwashs/cars.html'
    model = Car
    paginate_by = 8

    def get_context_data(self, *, object_list=None, **kwargs):

        return {
            **super().get_context_data(object_list=object_list, **kwargs),
            'car_form': kwargs.get('car_form', CarForm())
        }

    def post(self, request, *args, **kwargs):
        car_form = CarForm(request.POST)
        if car_form.is_valid():
            car_form.save()
            return redirect('wash:cars')
        context = self.get_context_data(car_form=car_form)
        return self.render_to_response(context)


class WasherDetailView(DetailView, FormMixin):
    form_class = OrderForm
    template_name = 'carwashs/washer-detail.html'
    context_object_name = 'washer'
    queryset = User.objects.filter(status=User.Status.washer)
    model = User

    def get_success_url(self):
        return self.object.get_absolute_url()

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        order_form = self.get_form()
        if order_form.is_valid():
            order: Order = order_form.save(commit=False)
            order.employee_id = self.object.pk
            try:
                start_date = datetime.strptime(
                    " ".join([
                        order_form.cleaned_data['start_date_day'],
                        order_form.cleaned_data['start_date_time']
                    ]),
                    '%d/%m/%Y %H:%M'
                )
                order.start_date = start_date
                order.save()
                return self.form_valid(form=order_form)
            except ValueError:
                order_form.add_error('start_date_day', 'please, enter correct data ')
        return redirect('wash:washer-detail', pk=self.object.pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        earned_money_q = ExpressionWrapper(
            F('price') * F('employee__salary') / Decimal('100.0'),
            output_field=DecimalField()
        )
        now = timezone.now()
        washer_salary_info: Dict[str, Optional[Decimal]] = self.object.orders.filter(end_date__isnull=False) \
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
        return {'order_form': kwargs.get('order_form', OrderForm()), **context, **washer_salary_info}
