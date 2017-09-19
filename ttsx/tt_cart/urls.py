from django.conf.urls import  url
from . import views

urlpatterns = [
    url(r'^$',views.index),
    url(r'^edit/$',views.edit),
    url(r'^add/$',views.add),
    url(r'^delcart/$',views.delcart),
    url(r'^count/$',views.count)
]

