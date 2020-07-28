from django.shortcuts import render,redirect
from django.contrib import auth
from django.http import JsonResponse
from django.urls import reverse
def index(request):
    return render(request,'index.html')

from zyh4.forms import LoginForm,RegisterForm
def login(request):
    params = {}
    from1 = request.GET.get('from','')
    params['from1'] = from1
    if request.method == 'GET':
        loginform = LoginForm()
    else:
        #LoginForm传的参数是个字典！！！
        #直接用request.POST这样就直接将所有表单的信息传进去了
        loginform = LoginForm(request.POST)
        #如果登录成功重定向到主页，失败则携带着执行内部clean函数携带表单内容和错误信息返回登录页面
        if loginform.is_valid():
            user = loginform.cleaned_data['user']
            auth.login(request,user)
            if request.is_ajax():
                return JsonResponse({'status': 'success'})
            return redirect(request.GET.get("from",reverse('index')))
        else:
            if request.is_ajax():
                return JsonResponse({'status': 'error','errormsg':'用户名或密码错误'})
            else:
                pass
    params['loginform'] = loginform
    return render(request, 'login.html', params)

def loginout(request):
    if request.method == 'POST':
        auth.logout(request)
        url = request.GET.get('from',reverse('index'))
        return redirect(url)

from django.contrib.auth.models import User
def register(request):
    params = {}
    from1 = request.GET.get('from','')
    params['from1'] = from1
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        registerform = RegisterForm(request.POST)
        if registerform.is_valid():
            user = User.objects.create_user(username=username,password=password,is_staff=False,is_superuser=False,email=email)
            user.save()
            user1 = auth.authenticate(username=username,password=password)
            auth.login(request,user1)
            url = request.GET.get('from')
            if not url:
                url = reverse('index')
                return redirect(url)
            else:
                return redirect(url)
    else:
        registerform = RegisterForm()
    params['registerform'] = registerform
    return render(request,'register.html',params)
























