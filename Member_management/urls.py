from django.urls import path
from . import views

app_name = 'member_management'

urlpatterns = [
    path('search_member/',views.search_member, name='search_member'),
    path('delete_member/',views.delete_member, name='delete_member'),
    path('email_search_member/',views.email_search_member, name='email_search_member'),
] 