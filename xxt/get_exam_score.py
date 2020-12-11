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
        'Cookie': 'source=""; lv=0; fid=11889; _uid=143186179; uf=b2d2c93beefa90dcdcba185928a24bfffa0214c848e99fd8630ec718d45a257cce7d9a0ef5e224a87abcdd2aa0f5ad19dc436c455fddffc288b83130e7eb47045ac8670337949add95e6357d4b6573c6b027a337608be8d61a2a387d7c92740e4131f8e6153a856fe7fafd565af53bf2; _d=1607692015003; UID=143186179; vc=D739C359B293732AC3ED20C635D096EE; vc2=E7B1CD3AAD469A65CF3FFE67662D92D6; vc3=A5jBNoYn%2BFkqSsKnED00JYj0peYIgnRhBBiUKHR6tDlzj4YQARk6HP12Pl6rS7NFgWSQS1mT4SVymCN29ztQ69MaJ%2BMkmBvQCtIGePGkCO5FpPjV3aZDd2SU6Qf47Ddez3pJ8JL5BlomJGd24yZHKKv3heCFP4dlNiQKmja3ks0%3D523796bf55bbcb9316943cf80366fe07; xxtenc=60b8f8a9b2998d7aae9cc36dbd81f260; DSSTASH_LOG=C_38-UN_13588-US_143186179-T_1607692015005; spaceFid=11889; spaceRoleId=3; JSESSIONID=73AE2A9E3E4CFEDA9E87349C44AA6439.CurriculumService; route=fd27a25a8235928f99e419cf06dbc48d',
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




