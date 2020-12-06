from django.shortcuts import render,redirect,reverse
from django.http import JsonResponse
import re,time
from xxt.aescryptor import *
import random,string
from PIL import Image,ImageDraw,ImageFont
from xxt.get_exam_score import fetch_person_score
from xxt.models import Xxt
from hashlib import md5
# Create your views here.
def get_client_ip(request):
    try:
        real_ip = request.META['HTTP_X_FORWARDED_FOR']
        regip = real_ip.split(",")[0]
    except:
        try:
            regip = request.META['REMOTE_ADDR']
        except:
            regip = ""
    return regip
def get_score_page(request):
    if not request.session.get('auth_key',''):
        request.session['auth_key'] = 'zyhabcd'
    else:
        if request.session['auth_key'] != 'zyhabcd':
            request.session['auth_key'] = 'zyhabcd'
    c_s = request.COOKIES.get('se_key','')
    c_n = request.COOKIES.get('n','')
    if c_s and c_n:
        if is_cookie_valid(c_n,c_s):
            return redirect(reverse('xxt:get_score_main_page'))
    return render(request,'xxt/xxt_authenticate.html')

def is_cookie_valid(s,se_key):
    num = decrypt(s.encode())
    try:
        num_str = re.findall(r'<(.*?)>',num)[0]
        num_list = num_str.split('x')
        num_list = list(map(lambda x:int(x),num_list))
        auth_key = se_key[num_list[0]] + se_key[num_list[1]] + se_key[num_list[2]]

    except:
        return False
    if auth_key == 'zyh':
        return True
    else:
        return False


def get_auth_status(request):
    if request.method == 'POST':
        if request.session.get('auth_key','') == 'zyhabcd':
            a = request.POST.get('a','')
            b = request.POST.get('b','')
            s_num = [5,9,16]
            a_key = ''.join([a[i] for i in range(len(a)) if i in s_num])
            b_key = ''.join([b[i] for i in range(len(b)) if i in s_num])
            if a_key == 'zyh' and b_key == 'zyh':
                url_page = reverse('xxt:get_score_main_page')
                res = JsonResponse({'status':1,'url':url_page})
                d = a + b
                se_key = re.sub(r';|:|t|T|s|k','',d)

                z_num = se_key.index('z')
                y_num = se_key.index('y')
                h_num = se_key.index('h')
                k = f"<{z_num}x{y_num}x{h_num}>" + str(time.time())

                encrypt_key = encrypt(k).decode()
                res.set_cookie('se_key',se_key,max_age=86400)
                res.set_cookie('n',encrypt_key,max_age=86400)
                return res
            else:
                return JsonResponse({'status':0,'error':'key_error'})

        else:
            return JsonResponse({'status':0,'error':'s_error'})
    else:
        return JsonResponse({'status':0,'error':'method error'})

def get_score_main_page(request):
    c_s = request.COOKIES.get('se_key','')
    c_n = request.COOKIES.get('n','')
    if c_s == '' or c_n == '':
        return redirect(reverse('xxt:get_score_page'))
    else:
        if is_cookie_valid(c_n, c_s):
            return render(request,'xxt/xxt_score_page.html')
        else:
            return redirect(reverse('xxt:get_score_page'))

def get_score(request):
    if request.method == 'POST':
        c_s = request.POST.get('se_key', '')
        c_n = request.POST.get('n', '')
        if request.session['vcodeverify'].lower() == request.POST.get('vcode','').lower():
            if is_cookie_valid(c_n,c_s):
                salt = '<zyh& {}55441as**&%^342~~~safs351'
                salt = salt + str(time.time()) + '&'
                enc_salt = encrypt(salt)
                course_url = request.POST.get('course_url','')
                try:
                    course_url_bak = course_url + '&'
                    courseid = re.findall(r'courseId=(.*?)&', course_url_bak,re.I)[0]
                    try:
                        classid = re.findall(r'clazzid=(.*?)&', course_url_bak,re.I)[0]
                    except:
                        classid = re.findall(r'classid=(.*?)&', course_url_bak, re.I)[0]
                    cpi = re.findall(r'cpi=(.*?)&', course_url_bak,re.I)[0]
                except:
                    return JsonResponse({'status': 0, 'error': 'please check your course url'})
                all_data = courseid + ',' + classid + ',' + cpi
                all_data_enc = encrypt(all_data).decode()
                full_url_md5 = md5(enc_salt).hexdigest()
                url = '/xxt/showscore/' + full_url_md5 + '?url=' + all_data_enc
                course_url_md5 = md5(all_data_enc.encode()).hexdigest()
                a = Xxt()
                a.xxt_full_url = full_url_md5
                a.xxt_course_url = course_url_md5
                a.save()
                return JsonResponse({'status':1,'url':url})
            else:
                return JsonResponse({'status': 0, 'error': 'params error'})
        else:
            return JsonResponse({'status': 0,'error':'验证码错误'})
    else:
        return JsonResponse({'status': 0,'error':'method error'})

def show_score(request,secret_key):
    t = Xxt.objects.filter(xxt_full_url=secret_key)
    if list(t) == []:
        return JsonResponse({'status':0,'error':'secret_key not be found'})
    t_data = t[0]
    course_url = request.GET.get('url', '')
    course_url_md5 = md5(course_url.encode()).hexdigest()
    if t_data.xxt_course_url == course_url_md5:
        ip = get_client_ip(request)
        #showscore中的c_enc需要解密两次
        params = {"c_enc":encrypt(course_url).decode(),'ip':ip}
        return render(request,'xxt/xxt_show_score.html',params)
    else:
        return JsonResponse({'status':0,'error':'secret_key error'})

def get_all_score_data(request):
    if request.method == 'POST':
        all_params = request.POST.get('c','')
        try:
            d_1 = decrypt(all_params.encode())
            d_2 = decrypt(d_1.encode())
            courseid,classid,cpi = d_2.split(',')
        except:
            return JsonResponse({'status': 0, 'error':'params error'})
        try:
            all_data = fetch_person_score(courseid,classid,cpi)
        except:
            return render(request,'500.html')
        return JsonResponse({'status':1,'data':all_data})
    else:
        return JsonResponse({'status': 0, 'error': 'method error'})

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def private_score_page(request):
    if request.method == "POST":
        token = request.POST.get("token","")
        url = request.POST.get("url", "")
        # get_data(token,url,"9eef43b46e423f88c9837b206da1b25d")
        auth_key = "9eef43b46e423f88c9837b206da1b25d"
        if token == auth_key:
            if url:
                try:
                    course_url_bak = url + '&'
                    courseid = re.findall(r'courseId=(.*?)&', course_url_bak, re.I)[0]
                    try:
                        classid = re.findall(r'clazzid=(.*?)&', course_url_bak, re.I)[0]
                    except:
                        classid = re.findall(r'classid=(.*?)&', course_url_bak, re.I)[0]
                    cpi = re.findall(r'cpi=(.*?)&', course_url_bak, re.I)[0]
                    try:
                        all_data = fetch_person_score(courseid, classid, cpi)
                        return JsonResponse({'status': 1, 'data': all_data})
                    except:
                        return JsonResponse({'status': 0, 'error': '请联系管理员'})

                except:
                    return JsonResponse({'status': 0, 'error': 'please check your course url'})
            else:
                return JsonResponse({'status': 0, 'error': 'empty url'})
        else:
            return JsonResponse({'status': 0, 'error': 'token error'})
    else:
        token = request.GET.get("token","")
        params = request.GET.get("params","")
        if token == "zyh123456":
            if params:
                try:
                    courseid,classid,cpi = params.split(",")
                    try:
                        all_data = fetch_person_score(courseid, classid, cpi)
                        return JsonResponse({'status': 1, 'data': all_data})
                    except:
                        return JsonResponse({'status': 0, 'error': '请联系管理员'})

                except:
                    return JsonResponse({'status': 0, 'error': 'please check your params'})
            else:
                return JsonResponse({'status': 0, 'error': 'empty params'})
        else:
            return JsonResponse({'status': 0, 'error': 'token error'})


def createvcode(request):
    #创建画布
    width = 100
    height = 50
    im_color = (random.randrange(20,100),random.randrange(20,100),random.randrange(20,100))
    im = Image.new(mode='RGB',size=(width,height),color=im_color)
    #创建画笔，让画笔绑定一个画布
    drawpen = ImageDraw.Draw(im)
    #开始画点,画100个点
    for i in range(0,100):
        #定义坐标
        xy = (random.randrange(0,width),random.randrange(0,height))
        #定义颜色
        fillcolor = (random.randrange(0,255),255,random.randrange(0,255))
        #开始画点,用point画点
        drawpen.point(xy,fill=fillcolor)
    import string
    code_str = string.ascii_letters + string.digits
    vcode = ''
    for i in range(0,4):
        vcode += code_str[random.randrange(0,len(code_str))]
    request.session['vcodeverify'] = vcode
    #设置字体
    font = ImageFont.truetype('DejaVuSerif.ttf',40)
    #开始写内容
    color1 = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
    color2 = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    color3 = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    color4 = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    drawpen.text((5,2),vcode[0],font=font,fill=color1)
    drawpen.text((25, 2), vcode[1],font=font,fill=color2)
    drawpen.text((50, 2), vcode[2],font=font, fill=color3)
    drawpen.text((75, 2), vcode[3],font=font, fill=color4)
    #画笔用完之后就销毁
    del drawpen
#先写入内存，然后再传入response
#linux下有奇效
    import io
    from django.http import HttpResponse
    buf = io.BytesIO()
    #以png格式储存
    im.save(buf,'png')
    return HttpResponse(buf.getvalue(),'image/png')











