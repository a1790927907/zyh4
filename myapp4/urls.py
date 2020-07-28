from django.conf.urls import url
from myapp4.views import *
urlpatterns = [
    url(r'^index/$',index),
    url(r'(\d+)$',showarticle,name='showarticle'),
]