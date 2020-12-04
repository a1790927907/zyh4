import json
import re
import asyncio
import aiohttp
#https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-list?clazzid=32311120&courseid=214717081&cpi=142139892&ut=s&page=1&pageSize=16&personId=72885916

async def fetch_name(courseid,classid,cpi,headers):
    name_url = 'https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-stastics?courseid=' + str(
        courseid) + '&clazzid=' + str(classid) + '&personId=' + str(cpi) + '&score=100&cpi=142139892&ut=s&'
    try:
        async with aiohttp.ClientSession() as session:
            res = await session.get(name_url,headers=headers)
            text = await res.text()
            name = re.findall(r'class="user-name">(.*?)</h3>', text)[0]
            res.close()
    except:
        try:
            async with aiohttp.ClientSession() as session:
                res = await session.get(name_url, headers=headers)
                text = await res.text()
                name = re.findall(r'class="user-name">(.*?)</h3>', text)[0]
                res.close()
        except:
            name = "未知"

    return name

async def fetch_data_info(courseid,classid,cpi,headers,page):
    url = 'https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-list?clazzid=' + str(classid) + '&courseid=' + str(
        courseid) + '&cpi=142139892&ut=s&page=' + str(page) + '&pageSize=16&personId=' + str(cpi)
    try:
        async with aiohttp.ClientSession() as session:
            res = await session.get(url,headers=headers)
            text = await res.text()
            data = json.loads(text)['data']
    except:
        async with aiohttp.ClientSession() as session:
            res = await session.get(url, headers=headers)
            text = await res.text()
            data = json.loads(text)['data']
    return data


async def _fetch_person_score(courseid,classid,cpi):
    headers = {
        'Cookie': 'source=""; lv=0; fid=11889; _uid=143186179; uf=b2d2c93beefa90dcdcba185928a24bfffa0214c848e99fd8630ec718d45a257cce7d9a0ef5e224a819a4864e13337d1630d92481d752d66f88b83130e7eb47045ac8670337949add95e6357d4b6573c6b027a337608be8d671189893cc17245795fb9ff8d7fc6b15e7fafd565af53bf2; _d=1607059797324; UID=143186179; vc=D739C359B293732AC3ED20C635D096EE; vc2=2A0C81325B6A72038EF22A3CE87FCB1B; vc3=AR09lwt6kuZpMu%2F6d%2F7WS3vdEmh3IpJMI5O9pCEtl6PHu4eUywR4o6axftWS894eO%2FOZmm2MnbD04XAbUSKsqjftVVFYS0y1C6r3phK2BHuL6SNh0Eh2Y8shebbWH3obtPEiOZEFZIru9r%2Fe%2BPzU%2FdF1bUfZ5PmlBWMT5qP37ak%3D6794dd2fda9654313f8bd0bf83a40c11; xxtenc=60b8f8a9b2998d7aae9cc36dbd81f260; DSSTASH_LOG=C_38-UN_13588-US_143186179-T_1607059797325; spaceFid=11889; spaceRoleId=3; k8s=30f29ddc6a1249a279f147d7833d82bd08af106f; jrose=35035C6F6A05A4F0DCB0473E34268161.mooc-statistics2-2996158868-kp1ht; route=f4530fc65c8934baba769156ca67ec88',
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    name_task = asyncio.create_task(fetch_name(courseid,classid,cpi,headers))
    name = ''
    page = 1
    all_data = []
    while True:
        data_task = asyncio.create_task(fetch_data_info(courseid,classid,cpi,headers,page))
        if not name:
            name = await name_task
        data = await data_task
        if data == []:
            break
        for exam_data in data:
            new_data = {}
            new_data['name'] = name
            new_data['title'] = exam_data['title']
            try:
                new_data['score'] = exam_data['stuScore']
            except:
                new_data['score'] = 0
            new_data['total'] = exam_data['totalScore']
            new_data['markPerson'] = exam_data['markPerson']
            all_data.append(new_data)
        page += 1
    return all_data

def fetch_person_score(courseid,classid,cpi):
    all_data = asyncio.run(_fetch_person_score(courseid,classid,cpi))
    return all_data


if __name__ == '__main__':
    import time
    now = time.time()
    print(fetch_person_score(206274073, 12494369 ,72885916))
    print(time.time()-now)




