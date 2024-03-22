from django.db import models
from django.core.validators import MaxValueValidator, RegexValidator


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='Дата обновления', auto_now=True)

    class Meta:
        abstract = True


class Goods(BaseModel):
    location_pick_up = models.ForeignKey(
        to='Location',
        verbose_name='Локация pick-up',
        on_delete=models.CASCADE,
        related_name='location_pick_up_goods'
    )
    location_delivery = models.ForeignKey(
        to='Location',
        verbose_name='Локация delivery',
        on_delete=models.CASCADE,
        related_name='location_delivery_goods'
    )
    weight = models.PositiveIntegerField(verbose_name='Вес', default=1, validators=[MaxValueValidator(1000)])
    description = models.CharField(verbose_name='Описание', max_length=999, null=True, blank=True)

    class Meta:
        db_table = 'goods'
        verbose_name = 'Груз'
        verbose_name_plural = 'Грузы'


class Car(BaseModel):
    unique_number = models.CharField(
        verbose_name='Уникальный номер',
        max_length=5,
        validators=[
            RegexValidator(
                regex='^[0-9]+[0-9]+[A-Z]$',
                message='Unique number not valid'
            )
        ]
    )
    current_location = models.ForeignKey(
        to='Location',
        on_delete=models.CASCADE,
        verbose_name='Текущая локация',
        related_name='current_location_car'
    )
    carrying = models.PositiveIntegerField(
        verbose_name='Грузоподъемность',
        default=1,
        validators=[MaxValueValidator(1000)]
    )

    class Meta:
        db_table = 'car'
        verbose_name = 'Машина'
        verbose_name_plural = 'Машины'


class Location(BaseModel):
    city = models.CharField(verbose_name='Город', max_length=50)
    state = models.CharField(verbose_name='Штат', max_length=100)
    zip_code = models.PositiveIntegerField(verbose_name='Почтовый индекс')
    latitude = models.FloatField(verbose_name='Широта')
    longitude = models.FloatField(verbose_name='Долгота')

    class Meta:
        db_table = 'location'
        verbose_name = 'Локация'
        verbose_name_plural = 'Локации'
