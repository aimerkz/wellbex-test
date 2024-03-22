from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('v1/goods/', views.CreateGoodsView.as_view(), name='list_create_goods'),
]
