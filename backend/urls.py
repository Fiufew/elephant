from django.urls import path

from . import views

app_name = 'backend'

urlpatterns = [
    path('', views.index, name='car_list'),
    path('car/create/', views.create_car, name='car_create'),
    path('car/<slug:slug>/', views.car_detail, name='car_detail'),
    path('car/<slug:slug>/edit/', views.edit_car, name='car_edit'),
    path('car/<slug:slug>/delete', views.remove_car, name='car_remove'),
    path('bids/', views.bid_list, name='bid_list'),
    path('bids/create/', views.create_bid, name='bid_create'),
    path('bids/<int:pk>/', views.bid_detail, name='bid_detail'),
    path('bids/<int:pk>/edit/', views.edit_bid, name='bid_edit'),
    path('bids/<int:pk>/delete', views.remove_bid, name='bid_remove'),
]
