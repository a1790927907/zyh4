from django.conf.urls import url
from blog.views import *
urlpatterns = [
    url(r'^allblogs$',allblogs,name='allblogs'),
    url(r'^showblog$',showblog,name='showblog'),
    url(r'^showtype$',showtypedetail,name='showtype'),
    url(r'^appreciate$',appreciate,name='appreciate'),
]



