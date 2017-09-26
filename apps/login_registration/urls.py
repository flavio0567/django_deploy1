from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^login$', views.login),
	url(r'^check_login$', views.check_login),
	url(r'^register$', views.register),
	url(r'^check_register$', views.check_register),
]
