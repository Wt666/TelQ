import requests
import time
import json

HEADERS_PORTAL = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36 Edg/94.0.992.47',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
    # 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    "Content-Type": "application/json",
    'authority': 'smsportal.jegotrip.com:8087',  # prod
    # 'authority': 'tsmsportal.jegotrip.com:8087', # stg
    'Host': '18.167.119.109:8087',  # STG
    'authorization': 'Basic ZXlKaGJHY2lPaUpJVXpVeE1pSXNJbWxoZENJNk1UWTBNVEUzTlRjNE9Dd2laWGh3SWpveE5qUXhNall5TVRnNGZRLmV5SjFhV1FpT2pFeE5pd2lkSGx3WlNJNk1UQXdMQ0p6WTI5d1pTSTZleUp5YjJ4bElqb2lRMDFKUVdSdGFXNVRZMjl3WlNJc0luTnRjeUk2TVN3aWRtOXBjQ0k2TVgxOS5SX3lvVU5QWmhXT2Y2TllFTThkVmk0OUZEbC1IbDFIcmxOSklMb1Frd3J5NjlXdTcwaWVrdV9wRWxKZUpDaXNNYkx1bDhVYkdEemxodXRtZmJFOUQydzo='
    # authorization是登录状态，具有时效性
}


def get_dict_all_price_list():
    # 获取各方向通道成本价格，用于添加物理通道
    url = 'https://smsportal.jegotrip.com:8087/sms/cost/template'  # prod
    # url = 'http://18.167.119.109:8087/sms/cost/template' # stg
    headers = HEADERS_PORTAL.copy()
    del headers['Content-Type']  # 因为使用get访问
    html = requests.get(url, headers=headers)
    print(html.text)
    html = json.loads(html.text)
    dict_all_price_list = {}  # dire:price_list
    dict_countryCode = {}
    for pl in html['data']:
        del pl["selling_price"]
        pl["isAdd"] = True
        dict_all_price_list[pl['region'].split('/')[1]] = pl
        dict_countryCode[pl['region'].split('/')[1]] = int(pl.get('region_code'))
    return dict_all_price_list




def gene_price_list(dires_need=None):
    ## 构建price_list，是创建物理通道的参数
    dict_all_price_list = get_dict_all_price_list()
    if dires_need:
        # 根据所需方向创建
        price_list = []
        for dire in dires_need:
            price_list.append(dict_all_price_list[dire])
    else:
        # 默认以所有方向创建
        price_list = list(dict_all_price_list.values())
    return price_list


def add_physical_channel(pname, code, supplier_id, dires_need=None):
    '''
    在portal平台添加物理通道
    :param pname: "PTMSCMI02"
    :param code: 'PTIMS-14128'
    :param supplier_id: "0"
    :param dires_need: ['China', 'Taiwan']
    "supplier_conn_type": 2 表示‘透传’，1表示‘直连’
    "billing_rules": 1表示SM计费，2表示DR计费
    :return:
    '''
    url = 'https://smsportal.jegotrip.com:8087/sms/cost/create'
    # url = 'http://18.167.119.109:8087/sms/cost/create'

    data = {"physical_channel": pname, "code": code, "code_type": "", "sms_agreement": "SMPP",
            "sms_type": "VerifyCode,Notification,Marketing", "supplier_id": supplier_id, "supplier_conn_type": 2,
            "name": pname, "billing_rules": 1,
            "price_list": gene_price_list(dires_need)}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)


def get_physicalChannel_id_v2(phyName='CPB99CMI02'):
    url = 'https://smsportal.jegotrip.com:8087/sms/physics/query'
    data = {"page": 1, "page_size": 10, "name": phyName}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    phyID = html['data']['list'][0]['id']
    return phyID


def get_physicalChannel_detail_v2(phyName='CPB99CMI02'):
    url = 'https://smsportal.jegotrip.com:8087/sms/physics/detail'
    data = {"physics_name": phyName}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    price_list = html['data']['cost_price_list']
    return price_list



##===============  业务通道基础操作
def get_businessChannel_id(business_Channel_Name='RTST057_API'):
    ### 业务通道基础信息，尤其是业务通道id, 可以用于查询业务通道detail
    ## 业务通道信息，特别包括 route_id
    url = 'https://smsportal.jegotrip.com:8087/sms/channel/query'
    data = {"page": 1, "page_size": 10, "name": business_Channel_Name, }
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    channel_id = html['data']['channel_list'][0]['id']
    channel_code = html['data']['channel_list'][0]['channel_code']
    english_name = html['data']['channel_list'][0]['english_name']
    route_id = html['data']['channel_list'][0]['route_id']
    return channel_id, channel_code, english_name, route_id


def businessChannel_create_v2(LName, business_Channel_Name, business_Name, dires_need):
    print(f'create_business_channel ing...')
    '''
    # v2 版本下，这是一个方向单组路由的代码
    # 在portal平台新建业务通道
    :param LName: ['CPB185CMI01', 'CPB185CMI02']
    :param note_name:'MTN_GlobalConnect_Solutions_Limited_-_A2P-14444'
    :param business_Channel_Name:"RTST01_API"
    :param business_Name:"RTST01"
    :return:
    '''
    url = 'https://smsportal.jegotrip.com:8087/sms/channel/create'

    dict_all_price_list = get_dict_all_price_list()  # 用于获取region
    # 构建 region_list
    # "region_list": [
    #     {"region": "泰国/Thailand", "master_physics": ["CPB34CMI04", "CPB141CMI02"],
    #      "master_send_ratio": [90, 10],
    #      "slave_physics": ["CPB34CMI03", "CPB141CMI01"], "slave_send_ratio": [90, 10]}]

    region_list = []
    for dire in dires_need:
        region = dict_all_price_list.get(dire).get("region")
        unit_dict = {"region": region,
                     "master_physics": [LName[1]], "master_send_ratio": [100],
                     "slave_physics": [LName[0]], "slave_send_ratio": [100]}
        region_list.append(unit_dict)
    data = {"physics_name": "", "name": business_Channel_Name,
            "p2p_type": 2, "sms_type": 2,
            "english_name": business_Name,
            "is_open": 2,
            "region_list": region_list}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    print(f'create_business_channel done.\n')


def get_businessChannel_detail_v2(channel_id):
    ### 查询业务通道detail，根据业务通道id
    ## 业务通道detail，特别包括 region_list，可用于modify业务通道参数,创建产品
    # channel_id = 222
    url = 'https://smsportal.jegotrip.com:8087/sms/channel/detail'
    data = {"channel_id": channel_id}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    region_list = html['data']['region_list']
    return region_list


def businessChannel_modify(AAA):
    # todo： 未开发使用

    url = 'http://18.167.119.109:8087/sms/cost/all'
    # 34: {account_id: 1, billing_rules: 1, channel: "CPB184CMI01", code: "MTN_GlobalConnect_Solutions_Li",…}
    # 35: {account_id: 1, billing_rules: 1, channel: "CPB184CMI02", code: "MTN_GlobalConnect_Solutions_Li",…}
    # account_id: 1
    # billing_rules: 1
    # channel: "CPB184CMI02"
    # code: "MTN_GlobalConnect_Solutions_Li"
    # code_type: ""
    # create_time: "2021-11-02 14:35:34"
    # id: 42
    # price_list: [{create_time: "2021-11-02 14:35:34", id: 6287, price: "0.088762", price_status: 1,…}, …]
    # sms_agreement: "SMPP"
    # sms_type: "VerifyCode,Notification,Marketing"
    # supplier_conn_type: 2
    # supplier_id: "11324"
    # update_time: "2021-11-02 14:35:34"

    # url = 'http://18.167.119.109:8087/sms/channel/detail'   # data = {"channel_id":376}
    # data: {channel_code: "0225502", create_time: "2021-11-02 14:35:36", english_name: "RTST01", id: 376,…}
    # channel_code: "0225502"
    # create_time: "2021-11-02 14:35:36"
    # english_name: "RTST01"
    # id: 376
    # is_open: 2
    # name: "RTST01_API"
    # p2p_type: 2
    # physics_channel: null
    # physics_detail: [,…]
    # 0: {channel_id: 376, code: "MTN_GlobalConnect_Solutions_Li", id: 13576, physics_channel: "CPB184CMI01",…}
    # 1: {channel_id: 376, code: "MTN_GlobalConnect_Solutions_Li", id: 13578, physics_channel: "CPB184CMI01",…}
    # 2: {channel_id: 376, code: "MTN_GlobalConnect_Solutions_Li", id: 13583, physics_channel: "CPB184CMI01",…}
    # 3: {channel_id: 376, code: "MTN_GlobalConnect_Solutions_Li", id: 13585, physics_channel: "CPB184CMI01",…}
    # 4: {channel_id: 376, code: "MTN_GlobalConnect_Solutions_Li", id: 13586, physics_channel: "CPB184CMI01",…}
    # channel_id: 376
    # code: "MTN_GlobalConnect_Solutions_Li"
    # id: 13586
    # physics_channel: "CPB184CMI01"
    # region: "中国台湾/Taiwan"
    # region_channel_status: 1
    # sms_agreement: "SMPP"
    # sms_type: "VerifyCode,Notification,Marketing"
    # sms_type: 2
    # update_time: "2021-11-04 10:11:50"

    url = 'http://18.167.119.109:8087/sms/channel/modify'
    data = {"physical_channel": None, "name": "RTST01_API", "is_open": 2, "sms_type": 2, "channel_code": "0225502",
            "english_name": "RTST01", "p2p_type": 2, "channel_id": 376,
            "create_list": [
                {"physics_channel": "CPB184CMI01", "region": "中国澳门/Macau", "sms_agreement": "SMPP",
                 "sms_type": "VerifyCode,Notification,Marketing", "code": "MTN_GlobalConnect_Solutions_Li"}],
            "update_list": [],
            "delete_list": [
                {"region_channel_id": 13586, "region": "南苏丹/South Sudan", "code": "MZF01", "physics_channel": "MZF01",
                 "sms_type": "VerifyCode,Notification,Marketing", "sms_agreement": "SMPP"}]}

    # create_list
    data = {"name": "RTST01_API", "is_open": 2,
            "english_name": "RTST01", "p2p_type": 2, "channel_id": 376,
            "create_list": [
                {"physics_channel": "CPB184CMI01", "region": "中国台湾/Taiwan", "sms_agreement": "SMPP",
                 "sms_type": "VerifyCode,Notification,Marketing", "code": "MTN_GlobalConnect_Solutions_Li"}],
            "update_list": [],
            "delete_list": []}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)

    # delete_list
    data = {"name": "RTST01_API", "is_open": 2,
            "english_name": "RTST01", "p2p_type": 2, "channel_id": 376,
            "create_list": [],
            "update_list": [],
            "delete_list": [{"region_channel_id": 13583, "physics_channel": "CPB184CMI01", "region": "中国台湾/Taiwan",
                             "sms_agreement": "SMPP",
                             "sms_type": "VerifyCode,Notification,Marketing",
                             "code": "MTN_GlobalConnect_Solutions_Li"}]}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)

    # update_list
    data = {"name": "RTST01_API", "is_open": 2,
            "english_name": "RTST01", "p2p_type": 2, "channel_id": 376,
            "create_list": [],
            "update_list": [{"region_channel_id": 13597, "physics_channel": "CPB184CMI02", "region": "中国澳门/Macau",
                             }],
            "delete_list": []}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)


def businessChannel_modify_update_v2(business_Channel_Name='RTST020_API', region='Taiwan',
                                     LName=['JCCNCMI01', 'JCCNCMI02']):
    '''比如要修改"中国台湾/Taiwan"路由，变成CPB91CMI01，CPB91CMI02'''
    ## 查询业务通道，根据业务通道名
    channel_id, channel_code, english_name, _ = get_businessChannel_id(business_Channel_Name)
    physics_detail_list = get_businessChannel_detail_v2(channel_id)
    ## modify 业务通道, 需要构建三大list
    url = 'https://smsportal.jegotrip.com:8087/sms/channel/modify'
    create_list = []
    update_list = []
    delete_list = []

    for phy_unit in physics_detail_list:
        if region in phy_unit['region']:
            # 筛选所需要的key：value
            phy_unit = {key: value for key, value in phy_unit.items() if key in ['region_channel_id', 'physics_channel',
                                                                                 'region',
                                                                                 "master_physics", "master_send_ratio",
                                                                                 "slave_physics", "slave_send_ratio"]}
            print('before:', phy_unit)
            phy_unit["master_physics"] = [LName[1]]
            phy_unit["slave_physics"] = [LName[0]]
            print('after:', phy_unit)
            update_list.append(phy_unit)
    # 创建data，进行modify
    data = {"name": business_Channel_Name, "is_open": 2, "sms_type": 2, "channel_code": channel_code,
            "english_name": english_name, "p2p_type": 2, "channel_id": channel_id,
            "create_list": create_list,
            "update_list": update_list,
            "delete_list": delete_list
            }
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    print('modify done.')
    # {"update_list": [
    #     {"region": "泰国/Thailand", "master_physics": ["JCCNCMI02"], "master_send_ratio": ["100"],
    #      "slave_physics": ["JCCNCMI01"], "slave_send_ratio": ["100"], "region_channel_id": 33241},
    #     {"region": "印度尼西亚/Indonesia", "master_physics": ["JCCNCMI02"], "master_send_ratio": ["100"],
    #      "slave_physics": ["JCCNCMI01"], "slave_send_ratio": ["100"], "region_channel_id": 33242},
    #     {"region": "中国台湾/Taiwan", "master_physics": ["JCCNCMI02"], "master_send_ratio": ["100"],
    #      "slave_physics": ["JCCNCMI01"], "slave_send_ratio": ["100"], "region_channel_id": 33243}], }


def businessChannel_modify_update_multi_v2(business_Channel_Name='RTST020_API'):
    # todo：参数需要修改
    dps = {"Taiwan": ['CPB92CMI01', 'CPB92CMI02'],
           "Macau": ['CPB92CMI01', 'CPB92CMI02'],
           "Hong Kong": ['CPB100CMI01', 'CPB100CMI02'],
           }
    for region, LName in dps.items():
        businessChannel_modify_update_v2(business_Channel_Name, region, LName)
    print('businessChannel_modify_update_multi done.')


def businessChannel_modify_create_v2(business_Channel_Name='ALIBABA_RTST', dires_need=['Taiwan'],
                                     LName=['CPB329CMI01', 'CPB329CMI02']):
    '''特别用于创建多方向的业务通道，期间输出的log要注意 方向名没匹配上而没添加成功的情况
    v2版本，主要修改了unit_dict
    '''

    ## 查询业务通道，根据业务通道名
    channel_id, channel_code, english_name, _ = get_businessChannel_id(business_Channel_Name)
    channel_list = get_businessChannel_detail_v2(channel_id)
    region_existing = {channel.get('region'): 1 for channel in channel_list}

    ## modify 业务通道, 需要构建三大list
    url = 'https://smsportal.jegotrip.com:8087/sms/channel/modify'
    create_list = []
    update_list = []
    delete_list = []

    # 构建create_list
    dict_all_price_list = get_dict_all_price_list()
    for dire in dires_need:
        create_list = []
        if dict_all_price_list.get(dire):
            region = dict_all_price_list.get(dire).get("region")
            if region_existing.get(region):
                print(f'region:{region} is existing, do not add it again.')
                continue
            unit_dict = {"region": region, "master_physics": [LName[1]], "master_send_ratio": [100],
                         "slave_physics": [LName[0]], "slave_send_ratio": [100]}
            create_list.append(unit_dict)
            # 创建data，进行modify
            data = {"name": business_Channel_Name, "is_open": 2, "sms_type": 2, "channel_code": channel_code,
                    "english_name": english_name, "p2p_type": 2, "channel_id": channel_id,
                    "create_list": create_list,
                    "update_list": update_list,
                    "delete_list": delete_list
                    }
            data = json.dumps(data)
            html = requests.post(url, data=data, headers=HEADERS_PORTAL)
            print(html.text)
            print(f'{dire}, modify create done.')
        else:
            print(f'{dire} cannot be found out in portal. =================')
    print('modify create done.')

    # {"create_list": [
    #     {"region": "越南/Vietnam", "master_physics": ["JCCNCMI02"], "master_send_ratio": [100],
    #      "slave_physics": ["JCCNCMI01"], "slave_send_ratio": [100]},
    #     {"region": "巴基斯坦/Pakistan", "master_physics": ["JCCNCMI02"], "master_send_ratio": [100],
    #      "slave_physics": ["JCCNCMI01"], "slave_send_ratio": [100]}], }


def get_tenant_id(tenant_name="CMIPB"):
    ### 租户信息，尤其是租户id，可用于订购产品、发送记录查询
    if tenant_name == "CMIPB":  # 常用租户
        tenant_id = 27
        return tenant_id

    ## 根据租户名，查询租户id
    url = 'https://smsportal.jegotrip.com:8087/public/tenement/query'
    data = {"page": 1, "page_size": 10, "type": "", "name": tenant_name}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    for tenant_info in html["data"]["tenement_list"]:
        if tenant_info["tenement_name"] == tenant_name:  # 对租户名做校验,精确匹配
            return tenant_info["id"]
    # tenant_id = html["data"]["tenement_list"][0]["id"]
    print(f'can not find tenant_name exactly, {tenant_name}')


def get_product_id(product_name):
    ### 产品信息，尤其是产品id，可用于订购产品
    ## 根据产品名，查询产品id
    url = 'https://smsportal.jegotrip.com:8087/sms/product/query'
    data = {"page": 1, "page_size": 10, "product_name": product_name, "pay_type": 0}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    for product_info in html['data']['product_list']:
        if product_info['product_name'] == product_name:
            return product_info['id']
    print(f'can not find product_name exactly, {product_name}')
    # product_id = html['data']['product_list'][0]['id']
    # return product_id


def get_product_detail(product_name):
    url = "https://smsportal.jegotrip.com:8087/sms/product/detail"
    data = {"product_id": get_product_id(product_name)}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    return html


def create_prepaid_product_v2(business_Channel_Name='ALIBABA_RTST', product_name='ALIBABA_RTST_PACK002'):
    print(f'create_prepaid_product ing...')
    ### 根据业务通道，创建对应的短信预付费产品

    # business_Channel_Name = "RTST06_API"
    channel_id = get_businessChannel_id(business_Channel_Name)[0]

    # channel_id = 222
    physics_detail_list = get_businessChannel_detail_v2(channel_id)

    # product_name = "RTST06_PACK"
    url = 'https://smsportal.jegotrip.com:8087/sms/product/create'
    # 构建channel_list
    # channel_list = [
    #     {"master_physics": ["CPB34CMI04", "CPB141CMI02"],
    #      "master_physics_coding": ["Alibaba_Cloud_(Singapore)_Pte.", "Alibaba-14362"],
    #      "master_send_ratio": ["90", "10"], "master_sms_agreement": [2, 2],
    #      "master_sms_type": ["VerifyCode,Notification,Marketing", "VerifyCode,Notification,Marketing"],
    #      "region": "泰国/Thailand", "region_channel_status": 1, "slave_physics": ["CPB34CMI03", "CPB141CMI01"],
    #      "slave_physics_coding": ["Alibaba_Cloud_(Singapore)_Pte.", "Alibaba-14362"],
    #      "slave_send_ratio": ["90", "10"], "slave_sms_agreement": [2, 2],
    #      "slave_sms_type": ["VerifyCode,Notification,Marketing", "VerifyCode,Notification,Marketing"],
    #      "sale_price": "0.0047", "isAdd": False}]
    # del 'region_channel_id'
    # add 'isAdd' = False
    # add 'sale_price'

    channel_list = []
    for i in range(len(physics_detail_list)):
        unit_dict = physics_detail_list[i]
        unit_dict['sale_price'] = "0.01"
        unit_dict['isAdd'] = False
        # del unit_dict['region_channel_id']
        channel_list.append(unit_dict)
    data = {"product_name": product_name, "channel_id": channel_id, "pay_type": 1, "price_currency": "USD",
            "sale_price": 1,
            "total_num": 200, "use_valid_term": 30, "use_valid_term_unit": "天",
            "start_product_valid_term": "",
            "end_product_valid_term": "", "is_open": 2, "valid_time_type": 1,
            "channel_des": "undefined/undefined ()", "p2p_type": 2,
            "channel_list": channel_list}
    data = json.dumps(data)

    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    print(f'create_product done.\n')


def create_postpaid_product_v2(business_Channel_Name='ALIBABA_RTST', product_name='ALIBABA_RTST_PACK004',
                               dps={'Thailand': 0.08, 'Australia': 0.09}):
    print('create_postpaid_product ing...')
    '''根据业务通道，创建对应的短信后付费产品
    若通道方向不在价格dps里面，则不创建，表示创建失败，需要检查dps
    '''

    channel_id = get_businessChannel_id(business_Channel_Name)[0]
    region_list = get_businessChannel_detail_v2(channel_id)

    url = 'https://smsportal.jegotrip.com:8087/sms/product/create'
    # 构建 new_channel_list
    new_channel_list = []
    for channel_unit in region_list:
        # del channel_unit['region_channel_id']
        channel_unit['isAdd'] = False
        if dps.get(channel_unit['region'].split("/")[-1]):
            channel_unit['sale_price'] = dps.get(channel_unit['region'].split("/")[-1])
        else:
            # channel_unit['sale_price'] = channel_dict.get(channel_unit['region'])
            print(f'{channel_unit["region"]}:price not in dps, postpaid_product create failed.')
            return
        new_channel_list.append(channel_unit)
    data = {"product_name": product_name, "channel_id": channel_id, "pay_type": 2, "price_currency": "USD",
            "sale_price": 0, "total_num": 0, "use_valid_term": 0, "use_valid_term_unit": "月",
            "start_product_valid_term": "", "end_product_valid_term": "", "is_open": 2,
            "valid_time_type": 1, "channel_des": "undefined/undefined ()", "p2p_type": 2,
            "channel_list": new_channel_list}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    print(f'update_product done.\n')


def order_product(product_name, tenant_name='CMIPB', oder_derial_number=None):
    print(f'order_product ing...')
    tenement_id = get_tenant_id(tenant_name)
    product_id = get_product_id(product_name)

    # 产品订购
    url = 'https://smsportal.jegotrip.com:8087/sms/order/create'
    data = {"tenement_id": tenement_id, "product_id": product_id, "oder_derial_number": oder_derial_number,
            "force_reply_up": None}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    print(f'order_product done.\n')



if __name__ == "__main__":
    print('program begin...')

    # 修改业务通道'RTST020_API'中'Taiwan'方向的物理通道为['CPB92CMI01', 'CPB92CMI02']，用于sale price不变的通道更改
    # business_Channel_Name = 'JNTK_API'
    # region = 'Saudi Arabia'
    # LName = ['JNTKCMI01', 'JNTKCMI02']
    # businessChannel_modify_update(business_Channel_Name,region,LName)

    ##
    # business_Channel_Name = 'CmiCHNBNK_VerifyCode_MainPtl'
    # LName = ['CHNBNK02', 'CHNBNK01']
    # businessChannel_modify_create(business_Channel_Name, dires_need, LName)

    # update_postpaid_product_v2(old_product_name='CXY_PACK04', new_product_name='CXY_PACK06',
    #                            dps={'Thailand': 0.0052})

    # #=======
    # # update add 业务通道
    # fun_update_add_business_channel()

    # ======
    # update 后附费产品
    # fun_update_postpaid_product()
