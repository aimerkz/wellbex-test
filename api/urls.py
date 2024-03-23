from django.urls import path

from api import views

app_name = 'api'

urlpatterns = [
    path('v1/goods/', views.ListCreateGoodsView.as_view(), name='list_create_goods'),
    path('v1/goods/<int:id>/', views.RetrieveUpdateDeleteGoodsView.as_view(), name='list_detail_update_delete_goods'),
    path('v1/car/<int:id>/', views.UpdateCarView.as_view(), name='detail-update-car')
]
