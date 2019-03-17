from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^sendLocation/$', views.sendLocation, name='sendLocation'),
    url(r'^sendMsg/$', views.sendMsg, name="sendMsg")
]