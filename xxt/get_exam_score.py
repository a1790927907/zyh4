import requests
import json
import re
#https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-list?clazzid=32311120&courseid=214717081&cpi=142139892&ut=s&page=1&pageSize=16&personId=72885916

def fetch_person_score(courseid,classid,cpi):
    headers = {
        "Cookie":"JSESSIONID=9DB8593722DB78FB2D1990C257D11A51.CurriculumService; route=a8fbc6321c8ff79218099b06834a4993; source=""; lv=0; fid=11889; _uid=143186179; uf=b2d2c93beefa90dcdcba185928a24bfffa0214c848e99fd8630ec718d45a257c7ccf5bc91c3ab546e9a5a2e0ee8c5458428b5a98cdb27be888b83130e7eb47045ac8670337949add95e6357d4b6573c6b027a337608be8d6aab6ac75780d22ffd18873bd84c68931e7fafd565af53bf2; _d=1606367099815; UID=143186179; vc=D739C359B293732AC3ED20C635D096EE; vc2=C15355D432562624F6E6047C786007A7; vc3=PRxUyTQD9IDtZQ%2BN4u6YdqSh4RLKY45Ozqx6c2%2Fr1IQZQ0Ih1tOkCD478S3zJQA7AozPNBFy7WgVxFe2gwhOWEW2K62gKfkGMzP2uHYNfd5V9KjiOsJCBVrQDHFt8Zx82TLEw4k2u5hhaGLTPDRHZ3b%2FLxYLKtgWctrXtnkFjuI%3Ddfafa2f00b552113f851d3ab2567017b; xxtenc=60b8f8a9b2998d7aae9cc36dbd81f260; DSSTASH_LOG=C_38-UN_13588-US_143186179-T_1606367099818; spaceFid=11889; spaceRoleId=3; rt=-2; tl=1",
        "User-Agent":"Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36",
    }
    name_url = 'https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-stastics?courseid=' + str(courseid) + '&clazzid='+ str(classid) +'&personId=' + str(cpi) + '&score=100&cpi=142139892&ut=s&'
    res_name = requests.get(name_url,headers=headers)
    try:
        name = re.findall(r'class="user-name">(.*?)</h3>',res_name.text)[0]
    except:
        name = '未知'
    page = 1
    all_data = []
    while True:
        url = 'https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-list?clazzid='+ str(classid) + '&courseid='+ str(courseid) + '&cpi=142139892&ut=s&page='+ str(page) +'&pageSize=16&personId=' + str(cpi)
        res = requests.get(url,headers=headers)
        data = json.loads(res.text)['data']

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


if __name__ == '__main__':
    print(fetch_person_score(206274073, 12494369 ,72885916))










