from django.conf.urls import url
from . import views
urlpatterns=[
    url('place_order',views.order)
]