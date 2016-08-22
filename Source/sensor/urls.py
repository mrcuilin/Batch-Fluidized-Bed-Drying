from django.conf.urls import url,include
from . import views
from django.contrib import admin

urlpatterns = [
    
    url( r'RUN$', views.commandRun, name='RUN' ),
    url( r'STOP$', views.commandStop, name='STOP' ),
    url( r'DAYS$', views.dayList, name='DAYS' ),
    url( r'SESSIONS*$', views.sessionList, name='SESSIONS' ),
    url( r'DOWNLOAD*$', views.download, name='DOWNLOAD' ),
    url( r'SHOW*$', views.show, name='SHOW' ),
    url( r'SHOWRAW*$', views.showRaw, name='SHOWRAW' ),
    url( r'SHOWGRAPH*$', views.showGraph, name='SHOWGRAPH' ),
    url( r'STATUS$', views.result, name='STATUS' ),
    url( r'^$', views.result, name='result' ),
]
