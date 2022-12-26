from django.urls import path
from . import views

app_name = 'Order_management'
urlpatterns = [

    path('display_order_management/', views.display_order_management, name='display_order_management'),

    path('generate_rental/', views.generate_rental, name='generate_rental'), #整合顯示
    path('status_update_site/', views.status_update_site, name='status_update_site'), #確定場地付款（狀態更新為1）
    path('status_update_equ/', views.status_update_equ, name='status_update_equ'), #確定租借器材付款(狀態更新為1)  
    path('status_return_equ/', views.status_return_equ, name='status_return_equ'), #確定租借器材歸還(狀態更新為2)
    path('generate_rental2/', views.generate_rental2, name='generate_rental2'),


]