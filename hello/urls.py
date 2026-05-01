from django.urls import path
from hello import views
from hello.views import apartment_list

urlpatterns = [
    path("", views.home, name="home"),  # homepage
    path('apartments/', views.apartment_list, name='apartment_list'), # apartment list page
    path('apartments/add/', views.apartment_create, name='apartment_create'), # apartment creation page
    path('apartments/edit/<int:id>/', views.apartment_update, name='apartment_update'), # edit page
    path('apartments/delete/<int:id>/', views.apartment_delete, name='apartment_delete'), # delete page
    path('reserve/<int:id>/', views.reserve_apartment, name='reserve_apartment'), # reserve page
]
