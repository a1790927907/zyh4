from django.conf.urls import url
from wenku.views import *

urlpatterns = [
    url(r'^$',wenkuindex,name='wenkuindex'),
    url(r'^secretset$',cookieset,name='secretset'),
    url(r'^downloader$',downloader,name='downloader'),
    url(r'^documents/',documents,name='documents'),
    url(r'^removealleef5a335c7496abf0f701fbe1535df70bfee44abca9ac3d54d74102f9c601b46/',removefile),
]