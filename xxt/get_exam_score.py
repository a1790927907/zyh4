import requests
import json
import re
#https://stat2-ans.chaoxing.com/exam-stastics/stu-exam-list?clazzid=32311120&courseid=214717081&cpi=142139892&ut=s&page=1&pageSize=16&personId=72885916

def fetch_person_score(courseid,classid,cpi):
    headers = {
        "Cookie":"k8s=bebe388ba8a6e64a4fca2c010e07dcca26153be3; route=d4fc925c8d78ce1315b0eab056f65586; fanyamoocs=11401F839C536D9E; lv=0; fid=11889; _uid=143186179; uf=b2d2c93beefa90dcdcba185928a24bfffa0214c848e99fd8630ec718d45a257c7ccf5bc91c3ab546eebd91534f6817e3273683571faa0dcd88b83130e7eb47045ac8670337949add95e6357d4b6573c6b027a337608be8d6b3c5436619122d74f6fab6eedd253428e7fafd565af53bf2; _d=1606200466321; UID=143186179; vc=D739C359B293732AC3ED20C635D096EE; vc2=EE045C6383A358EBA238E835C5C6F9D3; vc3=M8mCcYRzG7lzs4%2BPLTP%2BDvoTdSmvg%2BB0MB6geWSl72ocQvIQqk1Fj4GZtB9V6QUCAp0ajQ5azqucMNwDacP8Lsmg34pBgsSDYjdh5cwMGrtcI8mk%2FGcGnqlwWmP1R1WAj2jltApK8zZ%2FKvUWYzBv6VVTnjini327uBqYHe7lcCc%3D3a3487e84a6d0e0b5319023bdf299ef7; xxtenc=60b8f8a9b2998d7aae9cc36dbd81f260; DSSTASH_LOG=C_38-UN_13588-US_143186179-T_1606200466322; thirdRegist=0; source=""; spaceFid=11889; spaceRoleId=3; jrose=7AEAAD8B6426A579B7AFA1FDAC29FA65.mooc-statistics2-4172530066-cqb7z",
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
        print(res.text)
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
    print(fetch_person_score(202433585, 11173297 ,72885916))










