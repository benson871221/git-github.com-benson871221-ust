from django.urls import path
from . import views

app_name = 'rental'
urlpatterns = [
    path('home_page/', views.home_page, name='home_page'),
    path('search_site/', views.search_site, name='search_site'),
    path('display_reserve_site/', views.display_reserve_site, name='display_reserve_site'),
    path('reserve_site/', views.reserve_site, name='reserve_site'),
    path('back_to_search_site/', views.back_to_search_site, name='back_to_search_site'),
    path('search_equipment/', views.search_equipment, name='search_equipment'),
    path('display_reserve_equipment/', views.display_reserve_equipment, name='display_reserve_equipment'),
    path('reserve_equipment/', views.reserve_equipment, name='reserve_equipment'),
    path('back_to_search_equipment/', views.back_to_search_equipment, name='back_to_search_equipment'),
    path('current_rental_record/', views.current_rental_record, name='current_rental_record'),
    path('delete_reserve_site/', views.delete_reserve_site, name='delete_reserve_site'),
    path('delete_reserve_equipment/', views.delete_reserve_equipment, name='delete_reserve_equipment'),
    path('historical_rental_record/', views.historical_rental_record, name='historical_rental_record'),

]