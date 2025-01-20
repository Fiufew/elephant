from django.urls import path

from . import views

app_name = 'backend'

urlpatterns = [
    path('', views.index, name='car_list'),
    path('car/create/', views.create_car, name='car_create'),
    path('car/<slug:slug>/', views.car_detail, name='car_detail'),
    path('car/<slug:slug>/edit/', views.edit_car, name='car_edit'),
    path('car/<slug:slug>/delete', views.remove_car, name='car_remove'),
    path('applications/', views.applications_list, name='applications'),
    path('applications/create/', views.create_application,
         name='application_create'),
    path('applications/<int:pk>/', views.application_detail,
         name='application_detail'),
    path('applications/<int:pk>/edit/', views.edit_application,
         name='application_edit'),
    path('applications/<int:pk>/delete/', views.remove_application,
         name='application_remove'),
]
