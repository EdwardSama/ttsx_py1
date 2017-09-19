from django.conf.urls import include, url
from . import views


urlpatterns = [
    url(r'^register/$',views.register),
    url(r'^login/$',views.login),
    url(r'^register_handle/$',views.register_handle),
    url(r'^login_handle/$',views.login_handle),
    url(r'^register_exist/$',views.register_exist),
    url(r'^info/$',views.info),
    url(r'^order(\d*)/$',views.order),
    url(r'^site/$',views.site),
    url(r'^logout/$',views.login_out),
    url(r'^active/$',views.active),
    url(r'^pay/$',views.pay),
    ]