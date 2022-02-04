import requests
import time
import json
import pandas as pd
import traceback
import sys

HEADERS_PORTAL = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    "Content-Type": "application/json",
    'authority': 'smsportal.jegotrip.com:8087',  # prod
    # 'authority': 'tsmsportal.jegotrip.com:8087', # stg
    'Host': '18.167.119.109:8087',  # STG
    'authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWTBNVGsyTnpFek1Dd2laWGh3SWpveE5qUXlNRFV6TlRNd2ZRLmV5SjFhV1FpT2pFeE5pd2lkSGx3WlNJNk1UQXdMQ0p6WTI5d1pTSTZleUp5YjJ4bElqb2lRMDFKUVdSdGFXNVRZMjl3WlNJc0luTnRjeUk2TVN3aWRtOXBjQ0k2TVgxOS5mcjVoWWVWbzdfX1ZoN3JfUng5a2hzNjJmN19UN0VQNzJjYVNEYUlPTFEzYVFFS1lKQmxTZmlJdmtaY2RDem1XbENVbnU5RWJWMEFqcndpMWo4Y0lfUTo='
    # authorization是登录状态，具有时效性
}

data = {"data": [{"account": "Boyce", "id": 10}, {"account": "Mgr_Betty", "id": 43}, {"account": "Mgnr_Zoey", "id": 97}, {"account": "Mngr_CindyL", "id": 132}, {"account": "SamuelZhi", "id": 225}, {"account": "Mngr_Tong", "id": 238}, {"account": "Mngr_Allan", "id": 239}, {"account": "Mngr_Martin", "id": 242}, {"account": "Janet_HSU", "id": 250}, {"account": "Daniel_QIAO", "id": 251}, {"account": "May_YIP", "id": 252}, {"account": "Jimmy_NI", "id": 253}, {"account": "Cindy_LIU", "id": 254}, {"account": "Betty_BAI", "id": 255}, {"account": "Jackie_CHEN", "id": 256}, {"account": "Allan_ZHENG", "id": 257}, {"account": "Jun_MA", "id": 258}, {"account": "Kevin_KWAN", "id": 259}, {"account": "Luke_LU", "id": 260}, {"account": "WOON_Kok_Lun", "id": 261}, {"account": "Andy_SHAO", "id": 262}, {"account": "Michael_SIAW", "id": 263}, {"account": "Vincent_Wang", "id": 264}, {"account": "Aaron_SANTOS", "id": 265}, {"account": "Kit_LO", "id": 266}, {"account": "Zoey_CHENG", "id": 267}, {"account": "Oscar_LIU", "id": 268}, {"account": "Chris_CHANG", "id": 269}, {"account": "YANG_Zhen", "id": 270}, {"account": "Phil_FANG", "id": 271}, {"account": "Karen_LEE", "id": 272}, {"account": "Ken_CHEN", "id": 273}, {"account": "GONG_Cheng", "id": 274}, {"account": "Kaku_GUO", "id": 275}, {"account": "KE_Yan", "id": 276}, {"account": "Helen_HE", "id": 277}, {"account": "Tomy_MA", "id": 278}, {"account": "Wade_QIN", "id": 279}, {"account": "Hobby_ZHONG", "id": 280}, {"account": "Ann_TSENG", "id": 281}, {"account": "Martin_HAN", "id": 282}, {"account": "Jotham", "id": 283}, {"account": "Dennis_LI", "id": 284}, {"account": "Wendy_WONG", "id": 287}, {"account": "Jamila", "id": 288}, {"account": "Mngr_CNX", "id": 325}, {"account": "ZHANG_Yibei", "id": 357}, {"account": "wangzhiming", "id": 380}, {"account": "liting_biz", "id": 381}, {"account": "zhoubo", "id": 382}, {"account": "qianxiaoj", "id": 383}, {"account": "zhangyibei", "id": 404}, {"account": "dennisli", "id": 405}, {"account": "jothamvarghese", "id": 406}, {"account": "andyzhang", "id": 407}, {"account": "martinhan", "id": 408}, {"account": "cyprienpogu", "id": 409}, {"account": "hobbyzhong", "id": 410}, {"account": "koklunwoon", "id": 423}, {"account": "haoranbai", "id": 424}], "error_code": 0, "msg": {"en-us": "Success", "zh-CN": "\u6210\u529f"}, "request": "GET /public/account/managers"}

managers = {}
for item in data['data']:
    managers[item['id']] = item['account']

## prod租户信息
## prod租户信息
url = 'https://smsportal.jegotrip.com:8087/public/tenement/query'
data = {"page": 1, "page_size": 400, "type": 2, "name": ""}  # 外部用户
data = json.dumps(data)
html = requests.post(url, data=data, headers=HEADERS_PORTAL)
print(html)
print(html.text)
html = json.loads(html.text)
tene = pd.DataFrame(html["data"]["tenement_list"])
tene = tene[['id', 'tenement_name', 'tenement_full_name']]
tene_ids = tene['id']
tene_manages = []
try:
    for tene_id in tene_ids:
        tene_manage = []
        # 查看租户的产品订购信息
        url = 'https://smsportal.jegotrip.com:8087/public/tenement/detail'
        data = {"tenement_id":tene_id}
        data = json.dumps(data)
        for _ in range(100):
            html = requests.post(url, data=data, headers=HEADERS_PORTAL)
            if html.status_code == 200:
                break
            else:
                print(html)
        html = json.loads(html.text)
        print(html)
        if html.get('data'):
            if html["data"].get("tenement_sms_dict"):
                manager_ids = html["data"]["tenement_sms_dict"]["manager_ids"]  # STG租户的产品订购信息
            elif html["data"].get("tenement_voip_dict"):
                manager_ids = html["data"]["tenement_voip_dict"]["manager_ids"]
            else:
                manager_ids = []
        else:
            manager_ids = []
        for mid in manager_ids:
            tene_manage.append(managers.get(mid))
        tene_manages.append(tene_manage)
except Exception as e:
    print(f'try except info: {e.args}')
    traceback.print_exc()
    info = sys.exc_info()
    print(info)

