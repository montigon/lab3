"""DjPr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views


urlpatterns = [
    url(r'^main/', views.Main),
    url(r'^admin/', admin.site.urls),
    url(r'^todolists/$', views.getToDoList),
    url(r'^newauth/$', views.auth),
    url(r'^register/$', views.register),
    url(r'^todolists/(?P<pk>[0-9]+)/$', views.DetailTasklist),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/$', views.getTasks),
    url(r'^shared/', views.Shared),
    url(r'^todolists/(?P<list_id>[0-9]+)/tasks/(?P<pk>[0-9]+)/$', views.TaskDetail),
    url(r'^tags/$', views.getTags),
    url(r'^tags/(?P<pk>[0-9]+)/$', views.DetailTag),
    #url(r'^users/$', UserList.as_view()),
    #url(r'^users/(?P<pk>[0-9]+)/$', UserDetail.as_view()),
]
