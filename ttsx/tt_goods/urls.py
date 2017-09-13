<<<<<<< HEAD
#coding=utf-8
from django.conf.urls import url
from . import views

urlpatterns = [
    url('^$',views.index),
    url('^list(\d+)_(\d+)_(\d+)/$',views.list),
    url('^(\d+)/$',views.detail)
=======
from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^list/$',views.list),
    url(r'^detail/(\d+)/(\d+)/$',views.detail),
    url(r'^list/(\d+)/(\d+)/(\d+)/$',views.list)
>>>>>>> cc276266a0528abde2ba50f9af0ce6c2a8099869
]
