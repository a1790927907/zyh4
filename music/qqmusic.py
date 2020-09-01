import requests
import json,re
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36'
}
def becomevalid(filename):
    changed_name = filename
    invalid_list = list('？?\*|“<>:/\'\" ')
    for invalid_word in invalid_list:
        if invalid_word in filename:
            changed_name = changed_name.replace(invalid_word,'')
    return changed_name

def getmusicfile(sign,songmid):
    session = requests.session()

    url = 'https://u.y.qq.com/cgi-bin/musics.fcg?sign=' + sign + '&_=1596958045320'

    data = '{"req_0":{"module":"vkey.GetVkeyServer","method":"CgiGetVkey","param":{"guid":"3428190121","songmid":["'+ songmid + '"],"songtype":[0],"uin":"0","loginflag":0,"platform":"23","h5to":"speed"}},"comm":{"g_tk":5381,"uin":0,"format":"json","platform":"h5"}}'

    res = session.post(url, data=data, headers=headers)
    alldata = json.loads(res.text)
    url_head_list = alldata['req_0']['data']['sip']
    url_body = alldata['req_0']['data']['midurlinfo'][0]['purl']
    for url_head in url_head_list:
        url_head_list.remove(url_head)
        url_head = url_head.replace('\\',"")
        url_head_list.append(url_head)
    url_list = [(head + url_body) for head in url_head_list]
    title_res = requests.get(f'https://y.qq.com/n/yqq/song/{songmid}.html',headers=headers)
    try:
        title = re.findall(r'<title>(.*?)</title>',title_res.text)[0].replace(' - QQ音乐-千万正版音乐海量无损曲库新歌热歌天天畅听的高品质音乐平台！','').replace('&#45;','-')
    except:
        title = '未能获取标题'
    title = becomevalid(title)
    mpath = f'./static_all/file/{title}.mp3'
    mcontent = requests.get(url_list[0],headers=headers)
    try:
        with open(mpath,'wb') as f:
            f.write(mcontent.content)
    except:
        try:
            with open(mpath, 'wb') as f:
                f.write(mcontent.content)
        except:
            return 'error'
    return title

if __name__ == '__main__':
    # music_list = getmusicfile('zzamuy8ihtozuqsocm0ec34e350b35931b9ac25cbd3e22ee389','003g4pMq16jlC7')
    title_res = requests.get(f'https://y.qq.com/n/yqq/song/002eDlpu4U223F.html', headers=headers)
    print(title_res.text)
    # try:
    #     res = requests.get(music_list[0],headers=headers)
    # except:
    #     res = requests.get(music_list[1], headers=headers)
    # with open('music1.mp3','wb') as f:
    #     f.write(res.content)







