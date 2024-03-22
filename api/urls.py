from django.urls import include, path
from rest_framework import routers

from api import views


app_name = 'api'

urlpatterns = [
    path('v1/goods/', views.CreateGoodsView.as_view(), name='create_goods'),
]
