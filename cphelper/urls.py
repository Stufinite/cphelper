# -*- coding: utf-8 -*-
from django.conf.urls import url
from cphelper import views
urlpatterns = [
	url(r'^CourseOfDept/$', views.CourseOfDept, name='CourseOfDept'),
	url(r'^CourseOfTime/$', views.CourseOfTime, name='CourseOfTime'),
]