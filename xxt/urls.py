from django.conf.urls import url
from xxt.views import *

urlpatterns = [
    url(r'^$',get_score_page,name='get_score_page'),
    url(r'^auth$',get_auth_status,name='get_auth_status'),
    url(r'^score$',get_score_main_page,name='get_score_main_page'),
    url(r'^vcode$',createvcode,name='createvcode'),
    url('^getscore$',get_score,name='get_score'),
    url(r'^showscore/(\w+)$',show_score,name='show_score'),
    url(r'^getdata$',get_all_score_data,name='get_score_data')
]







