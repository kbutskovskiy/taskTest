from django.urls import path
from . import views
from django.urls import re_path

app_name = 'shop'

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('purchase/', views.purchase, name='purchase'),
    path('', views.index, name='index'),
    re_path(r'^add_to_cart/(?P<product_id>\d+)/$', views.add_to_cart, name='add_to_cart'),
    path('view_cart/', views.view_cart, name='view_cart'),
    re_path(r'^update_cart/(?P<cart_item_id>\d+)/(?P<action>increase|decrease)/$', views.update_cart, name='update_cart'),
    re_path(r'^remove_from_cart/(?P<cart_item_id>\d+)/$', views.remove_from_cart, name='remove_from_cart'),
    path('recharge_balance/', views.recharge_balance, name='recharge_balance'),
]