from django.conf.urls import url
from music.views import *
urlpatterns = [
    url(r'^$',index,name='mindex'),
    url(r'^getmurl/$',getmurl,name='getmurl'),
    url(r'^mdownload/$',mdownload,name='mdownload'),
]
