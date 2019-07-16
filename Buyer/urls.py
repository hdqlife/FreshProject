from django.urls import path,re_path
from Buyer.views import *

urlpatterns = [
    path('index/', index),
    re_path('list/(?P<type_id>\d+)/(?P<page>\d+)', shop_list),
    re_path('detail/(?P<com_id>\d+)/', detail),
    path('register/', register),
    path('login/', login),
    path('cart/', cart),
    path('userCenter/', userCenter),
    path('userCenterOrder/', userCenterOrder),
    path('userCenterSite/', userCenterSite),
    path('place_order/', place_order),
    path('Pay/',Pay),
]