# -*- coding: utf-8 -*-
from django.conf.urls import url
from sign import views_if, views_if_sec
from django.urls import path

app_name = 'sign'  # 添加APP名

# ex : /api/xxx
urlpatterns = [
    # guest system interface:
    path('add_event/', views_if.add_event, name='add_event'),
    path('add_guest/', views_if.add_guest, name='add_guest'),
    path('get_event_list/', views_if.get_event_list, name='get_event_list'),
    path('get_guest_list/', views_if.get_guest_list, name='get_guest_list'),
    path('user_sign/', views_if.user_sign, name='user_sign'),

    # security interface:
    path('sec_get_event_list/', views_if_sec.get_event_list, name='get_event_list'),
    path('sec_add_event/', views_if_sec.add_event, name='add_event'),
    # path('sec_get_guest_list/', views_if_sec.get_guest_list, name='get_guest_list'),
]