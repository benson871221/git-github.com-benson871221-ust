from django.urls import path
from . import views

app_name = 'member'
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('edit_member_profile/', views.edit_member_profile, name='edit_member_profile'),
    path('logout/', views.logout, name='logout')
]