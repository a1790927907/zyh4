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
        'Cookie': 'source=""; lv=0; fid=11889; _uid=143186179; uf=b2d2c93beefa90dcdcba185928a24bfffa0214c848e99fd8630ec718d45a257c0baeeff80650d08faf6b87ba23af7ac830d92481d752d66f88b83130e7eb47045ac8670337949add95e6357d4b6573c6a696d78956426448e0c2467e27983836b8d376f1776efc0ae7fafd565af53bf2; _d=1610633870304; UID=143186179; vc=D739C359B293732AC3ED20C635D096EE; vc2=D4D5E7D66DBC480C4FFF0BA0452E656E; vc3=RXrpe8RdRCNdZvv7SIDG54aYNEZKP%2Fd3ZHQek%2BRz9w2fWe8E3TZLAiLDIPNMETKFXKrqQLmXbMNHO5gahP3%2B4YslGaD%2B5pocsZPL1pDRcxN0fEwbG9umpBdMyB2XN%2BdY7yCSecIsiJk40BrEagE8ch9PHIBjzlUMXJekXzsf3l4%3De5d0eb99475b9e2efa566741f75071d1; xxtenc=60b8f8a9b2998d7aae9cc36dbd81f260; DSSTASH_LOG=C_38-UN_13588-US_143186179-T_1610633870305; spaceFid=11889; spaceRoleId=3; JSESSIONID=ADCFBD2CE55147FB4EC6590572D4AC6F.CurriculumService; route=353349bf0fa5580c2c23247980829e03',
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




