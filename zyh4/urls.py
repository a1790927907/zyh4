"""zyh4 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url,include
from django.contrib import admin
from zyh4.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    url(r'^adminzyhzoneZYHZONE/', admin.site.urls),
    url(r'^myapp4/',include('myapp4.urls',namespace='myapp4')),
    url(r'^blog/',include('blog.urls',namespace='blog')),
    url(r'^$',index,name='index'),
    url(r'^ckeditor/',include('ckeditor_uploader.urls')),
    url(r'^login/',login,name='login'),
    url(r'^loginout/',loginout,name='loginout'),
    url(r'^comments/',include('comments.urls',namespace='comments')),
    url(r'^register/',register,name='register'),
    url(r'^wenku/',include('wenku.urls',namespace='wenku')),
    url(r'^403page/',error403,name='403page'),
    url(r'^404page/',error404,name='404page'),
    url(r'^500page/',error500,name='500page'),
]

urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)