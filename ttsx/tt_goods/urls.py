from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^list/$',views.list),
    url(r'^detail/(\d+)/(\d+)/$',views.detail),
    url(r'^list/(\d+)/(\d+)/(\d+)/$',views.list)
]
