import json
import re
import asyncio
import aiohttp


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
        'Cookie': 'source=""; lv=0; fid=11889; _uid=143186179; uf=b2d2c93beefa90dcdcba185928a24bfffa0214c848e99fd8630ec718d45a257c0f50073571ce618fbc61d03b712a4f66d110c105546a283d88b83130e7eb47045ac8670337949add95e6357d4b6573c6b027a337608be8d6a98d0ab8000e7340960ef9125354e0b3e7fafd565af53bf2; _d=1608301615369; UID=143186179; vc=D739C359B293732AC3ED20C635D096EE; vc2=499CAFD5BD872EC704B1E8E3F404BE3C; vc3=UBWyKxO0VfP2%2Bhj2pTnfxUY%2BSAv2czpWMcEJjVKr8%2FUGPX4wHi1SfNtkuOhQv%2FVXknnSKto6At4DIWFoDIrMXhdD80yqWCXnn1oSfrHF2LlSKj6cN4WDZnsKEpaDKb8LcJH%2FOrt9aKWNJGynt5wZ08bUXefVYqrHJaPktbR7qTA%3D45750f04ea824a2de4201990fe9a3840; xxtenc=60b8f8a9b2998d7aae9cc36dbd81f260; DSSTASH_LOG=C_38-UN_13588-US_143186179-T_1608301615370; spaceFid=11889; spaceRoleId=3; rt=-2; tl=1; k8s=e66d5328add0c052c4f407b42b64742fbb150f7e; jrose=6C99E3BDE9590FEBA436DD5E9017D145.mooc-2179700257-swt1v; route=2fe558bdb0a1aea656e6ca70ad0cad20; thirdRegist=0',
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




