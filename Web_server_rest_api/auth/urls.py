from django.conf.urls import url, include
from . import views

app_name = 'auth'

urlpatterns = [
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^dashboard/$', views.dashboard, name='dashboard'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^blackSpot/$', views.blackSpot, name='blackSpot'),
    url(r'^logout/$', views.logout, name='logout'),
    url('^api/', include('auth.api.urls'), name='api'),
]