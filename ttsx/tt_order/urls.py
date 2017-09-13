from django.conf.urls import url
from . import views
urlpatterns=[
    url(r'^place_order/$',views.order),
    url(r'^place_order/user_center_order/$',views.center)
]