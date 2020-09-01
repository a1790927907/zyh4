from django.shortcuts import render
from music.aescryptor import *
import time
from music.wangyi import *
from music.qqmusic import *
# Create your views here.
def index(request):
    res = render(request,'music/index.html')
    salt = str(time.time())+'<{"zyh":"good man","salttwo":"{[|||===---^&#$@ASfsjafgash]}"}>'
    crypted_word = encrypt(salt + 'zyh<').decode()
    res.set_cookie('msecret',crypted_word)
    return res

import re
from django.http import JsonResponse
def getmurl(request):
    msecret = request.COOKIES.get('msecret','')
    decryped_word = decrypt(msecret.encode())
    decryped_list = re.findall(r'>(.*?)<',decryped_word)
    if request.method == 'POST' and decryped_list != []:
        twice_auth_word = decryped_list[0]
        if twice_auth_word == 'zyh':
            mtype = request.POST.get('mtype','')
            murl = request.POST.get('musicurln','')
            if murl == '':
                return JsonResponse({'status':'url empty'})
            if mtype == '':
                return JsonResponse({'status': 'type empty'})
            if mtype == 'wyymusic':
                murl_wyy = murl + "&"
                murl_wyy = murl_wyy.lower()
                songid = re.findall('id=(.*?)&',murl_wyy)
                if songid == []:
                    return JsonResponse({'status': 'please check your url whether you have id params'})
                else:
                    if '#' in songid[0]:
                        return JsonResponse({'status': 'check whether you mistake the music type'})
                mpath,title = getmusicurl(songid[0])
                return JsonResponse({'status':'success','url':f'/music/mdownload?title={title}'})
            elif mtype == 'qqmusic':
                try:
                    songmid = re.findall(r'song/(.*?).html', murl)[0]
                except:
                    try:
                        songmid = re.findall(r'songmid=(.*?)#', murl)[0]
                    except:
                        return JsonResponse({'status': 'please check your url whether you have songmid params'})
                if request.POST.get('errorwarn',''):
                    return JsonResponse({'status': 'please check your url whether you have songmid params'})
                sign = request.POST.get('sekey','')
                sign = sign.replace('MDAT~!','z').replace('ZYbp|%','c').replace('*a(d/v:wty;','a').replace('~##5fljfh8','e')
                title = getmusicfile(sign,songmid)
                if title == 'error':
                    return JsonResponse({'status': 'music name is not valid'})
                else:
                    return JsonResponse({'status':'success','url':f'/music/mdownload?title={title}'})
        else:
            return JsonResponse({'status': 'encrypt error'})
    else:
        return JsonResponse({'status': 'method error'},status=405)


from django.http import FileResponse
def mdownload(request):
    title = request.GET.get('title','')
    if title == '':
        return JsonResponse({'status':'title empty'})
    mpath = f'./static_all/file/{title}.mp3'
    file = open(mpath,'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    from django.utils.http import urlquote
    response['Content-Disposition'] = 'attachment;filename="%s"' % (urlquote(title + '.mp3'))
    return response







