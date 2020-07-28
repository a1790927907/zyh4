from django.conf.urls import url
from comments.views import *
urlpatterns = [
    url(r'^upload/$',comment,name='upload'),
    url(r'^mark/$',mark,name='mark'),
    url(r'^removemark/$',removemark,name='removemark'),
    url(r'^cappreciate$',appreciate,name='cappreciate'),
]