from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import render,reverse


class BlogMiddleWare(MiddlewareMixin):
    names = [reverse('blog:allblogs'),reverse('blog:showblog'),reverse('blog:showtype')]
    def process_request(self,request):
        for name in self.names:
            if name in request.get_full_path():
                if request.user.username != 'zyh':
                    return render(request,'namenotzyh.html')








