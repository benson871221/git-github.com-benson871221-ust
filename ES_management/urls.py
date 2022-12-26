from django.urls import path
from . import views

app_name = 'ES_management'
urlpatterns = [
    
    #首頁############################################
    path('home_page/', views.home_page, name='home_page'),
    path('back_to_home_page/', views.back_to_home_page, name='back_to_home_page'),
    #場地管理############################################
    path('site_management/', views.site_management, name='site_management'),
    path('add_site/', views.add_site, name='add_site'),
    path('display_edit_site/', views.display_edit_site, name='display_edit_site'),
    path('edit_site/', views.edit_site, name='edit_site'),
    path('delete_site/', views.delete_site, name='delete_site'),
    #器材管理############################################
    path('equipment_management/', views.equipment_management, name='equipment_management'),
    path('add_equipment/', views.add_equipment, name='add_equipment'),
    path('display_edit_equipment/', views.display_edit_equipment, name='display_edit_equipment'),
    path('edit_equipment/', views.edit_equipment, name='edit_equipment'),
    path('delete_equipment/', views.delete_equipment, name='delete_equipment'),
]
