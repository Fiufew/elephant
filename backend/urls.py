from django.urls import path

from . import views

app_name = 'backend'

urlpatterns = [
    path('', views.index, name='car_list'),
    path('price/list/', views.price_list, name='price_list'),
    path('create_price/<int:pk>/', views.create_price, name='create_price'),
    path('update_price/<int:pk>/', views.update_price, name='update_price'),
    path('car/create/', views.create_car, name='car_create'),
    path('car/<slug:slug>/', views.car_detail, name='car_detail'),
    path('car/<slug:slug>/edit/', views.edit_car, name='car_edit'),
    path('car/<slug:slug>/delete', views.remove_car, name='car_remove'),
    path('bids/', views.bid_list, name='bid_list'),
    path('bids/create/', views.create_bid, name='bid_create'),
    path('bids/<int:pk>/', views.bid_detail, name='bid_detail'),
    path('bids/<int:pk>/edit/', views.edit_bid, name='bid_edit'),
    path('bids/<int:pk>/delete', views.remove_bid, name='bid_remove'),
    path('bids/take_in_work/<int:pk>/', views.take_in_work,
         name='take_in_work'),
    path('file/<int:file_id>/delete/', views.delete_file, name='delete_file'),
]
