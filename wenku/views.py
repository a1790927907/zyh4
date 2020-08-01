from django.shortcuts import render
from django.http import HttpResponse,JsonResponse,FileResponse

# Create your views here.
import hashlib,time
def sha256encrypt(string):
    string = string.encode()
    return hashlib.sha256(string).hexdigest()


def wenkuindex(request):
    return render(request,'wenku/wkdownloader.html')

def cookieset(request):
    if request.user.is_superuser and request.user.is_authenticated and (request.method == 'POST'):
        response = JsonResponse({'status':'success'})
        response.set_cookie('secretkey',sha256encrypt(str(time.time()) + '%$[djoLosKK}{]'))
        request.session['secretkey'] = response.cookies['secretkey'].value
        return response
    else:
        return JsonResponse({'status':'error'})
from wenku.models import Wenku
import os
def documents(request):
    title = request.GET.get('title')
    file = open(f"{title}",'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    from django.utils.http import urlquote
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(title))
    return response

def removefile(request):
    for i,j,k in os.walk("."):
        for filename in k:
            os.remove(f"{filename}")
    return JsonResponse({'status':'removesuccess'})


from wenku.wkdownloader import *
def downloader(request):
    if request.COOKIES['secretkey'] == request.session['secretkey']:
        if request.method == 'POST':
            wkurl = request.POST.get('wkurl')
            daochutype = request.POST.get('wenbentype','txt')
            wenkutype = request.POST.get('wktype','bdwk')
            if wenkutype == 'bdwk':
                if daochutype == 'txt':
                    content, title = getdocwithtxt(wkurl)
                    if content == 'error':
                        return JsonResponse({'status': 'error', 'erromsg': '解析失败!检查文库链接是否出错'})
                    downloadurl = '/wenku/documents/?title='+ str(title) + '.txt'
                    return JsonResponse({'status':'success','downloadurl':downloadurl})
                elif daochutype == 'word':
                    content, title = getdocwithword(wkurl)
                    if content == 'error':
                        return JsonResponse({'status': 'error', 'erromsg': '解析失败!检查文库链接是否出错'})
                    downloadurl = '/wenku/documents/?title=' + str(title) + '.docx'
                    return JsonResponse({'status': 'success', 'downloadurl': downloadurl})
                else:
                    return JsonResponse({'status': 'typeerror'})
        else:
            return JsonResponse({'status': 'methoderror','erromsg':'请求方式出错'})
    else:
        return JsonResponse({'status': 'secretkeyerror','erromsg':'参数出错'})
























