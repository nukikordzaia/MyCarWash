from django.db import models
from django.forms import IntegerField
from django.utils.translation import ugettext_lazy as _


class CarType(models.Model):
    name = models.CharField(max_length=45, verbose_name=_('Car Type'), unique=True)
    price = models.DecimalField(max_digits=4, decimal_places=2)

    def __str__(self):
        return self.name


class WashType(models.Model):
    name = models.CharField(max_length=45, verbose_name=_('Car Type'), unique=True)
    percentage = models.IntegerField(verbose_name=_("Percentage of base price"), default=100)

    def __str__(self):
        return self.name


class Car(models.Model):
    car_type = models.ForeignKey(
        to='CarType',
        on_delete=models.SET_NULL,
        null=True, related_name='cars'
    )
    licence_plate = models.CharField(max_length=20, verbose_name=_("License plate"))

    def __str__(self):
        return self.licence_plate

    class Meta:
        verbose_name = _('Car')
        verbose_name_plural = _('Cars')


class Order(models.Model):
    car = models.ForeignKey(
        to='Car', related_name='orders',
        on_delete=models.PROTECT,
    )
    employee = models.ForeignKey(
        to='user.User', on_delete=models.SET_NULL,
        null=True, related_name='orders',
    )
    # @TODO: washer_percentage

    wash_type = models.ForeignKey(
        to='WashType', related_name='orders',
        on_delete=models.PROTECT,
    )

    note = models.TextField(null=True, blank=True, verbose_name=_("Note"))
    price = models.DecimalField(max_digits=4, decimal_places=2, verbose_name=_("Price"))

    created_date = models.DateTimeField(auto_now_add=True, verbose_name=_("Created date"))
    start_date = models.DateTimeField(verbose_name=_('Scheduled time'))
    end_date = models.DateTimeField(verbose_name=_('Scheduled time'))

    def __str__(self):
        return f'{self.car} using {self.wash_type}'

    class Meta:
        verbose_name = _('Order')
        verbose_name_plural = _('Orders')

    def save(self, *args, **kwargs):
        if not self.pk:
            self.price = self.car.car_type.price * self.wash_type.percentage / 100
        super(Order, self).save(*args, **kwargs)
