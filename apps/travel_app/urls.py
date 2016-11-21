from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^travels$', views.home),
    url(r'^logout$', views.logout),
    url(r'^travels/add$', views.add),
    url(r'^travels/destination/(?P<id>\d+$)', views.trip),
    url(r'^join/(?P<id>\d+$)', views.join),
    url(r'^create', views.create)
]
