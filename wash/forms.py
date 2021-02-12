from django.forms import ModelForm
from wash.models import CarType
from django.core.validators import MaxLengthValidator, RegexValidator
from django.forms import CharField, Textarea, ModelChoiceField, TextInput
from wash.models import Order, Car, WashType


class CarForm(ModelForm):
    car_type = ModelChoiceField(queryset=CarType.objects.all())
    licence_plate = CharField(max_length=20)

    class Meta:
        model = Car
        fields = '__all__'



class OrderForm(ModelForm):
    note = CharField(widget=Textarea(attrs={
        'id': 'icon_prefix2',
        'class': 'materialize-textarea'
    }), validators=[MaxLengthValidator(150)])
    car = ModelChoiceField(queryset=Car.objects.all())
    wash_type = ModelChoiceField(queryset=WashType.objects.all())
    start_date_day = CharField(widget=TextInput(attrs={
        'class': 'datepicker'
    }), validators=[RegexValidator(
        r'^(0[1-9]|[12][0-9]|3[01])[- /.](0[1-9]|1[012])[- /.](21|20)\d\d$',
        message='this is correct format: dd/mm/yyyy'
    )])
    start_date_time = CharField(widget=TextInput(attrs={
        'class': 'timepicker'
    }), validators=[RegexValidator(r'^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$', message='this is correct format: MM:HH')])

    class Meta:
        model = Order
        fields = ('car', 'wash_type', 'note', 'start_date_day', 'start_date_time',)
