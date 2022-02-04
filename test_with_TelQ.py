import datetime
import time

from telQ_basic import *
from send_SMS_api import send_sms
from analy_dispatchingLog import analy_dispatchingLog
routeTST_pRate_path = r'C:\Users\rexwang\Documents\routeTST_pRate.csv'

def send_test_Message(tests_Paras, countryCode, route_id, auth_key, senderID=None, ttextEnd=False):
    '''

    :param tests_Paras:
    :param countryCode:
    :param route_id:
    :param auth_key:
    :param senderID: 使用特定SenderID发短信
    :param ttextEnd: 将telQ的测试字段追加在短信内容末尾。否则替换指定内容，比如111111
    :return:
    '''
    templs = {
        # 8种：字母OA、数字OA，长短信、短信，中文、英文
        # "google": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goo1gle": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goo2gle": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goog3le": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goo4gle": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goo5gle": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goo6le": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "goog7le": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "googl8e": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "googl9e": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "google99": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "google999": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",
        # "google9999": "Llego el 111111 que solicito, haga clic en el enlace para ver：wa.me/919878847809",


        # "whatsapp": "[#][TikTok] 111111 is your verification code",
        # "Apple1": "[#][TikTok] 111111 is your verification code",
        # "Apple2": "[#][TikTok] 111111 is your verification code",
        # "Apple3": "[#][TikTok] 111111 is your verification code",
        # "Apple5": "[#][TikTok] 111111 is your verification code",
        # "Apple4": "[#][TikTok] 111111 is your verification code",
        # "Twitter": "[#][TikTok] 111111 is your verification code",
        #
        # "Google": "Your verification code is 111111",
        "CloudSMS": "Your verification code is 111111",
        "123456": "Your verification code is 111111",
        "Google": "Your pin code is 111111, please do not disclose it, if you have any question, please contact me, as the M800 cannot provide service, Vietnam is left empty, so I do not pick up your phone call,  best regard.",
        "234567": "Your pin code is 111111, please do not disclose it, if you have any question, please contact me, as the M800 cannot provide service, Vietnam is left empty, so I do not pick up your phone call,  best regard.",

        "cCloudSMS": "您的注册验证码为：111111",
        "345678": "您的验证码是111111。请注意保护您的验证码信息，不要分享给其他人。",
        "dloudSMS": "您的一次性验证码为 111111 ,请勿告知他人,谢谢。[今日知识]知识就像海洋，只有意志坚强的人才能到达彼岸。这是伟大的马克思的名言名句，送予意志坚强的你，希望继续坚持，早日登上理想的彼岸，regrads.",
        "456789": "您的一次性验证码为 111111 ,请勿告知他人,谢谢。[今日知识]知识就像海洋，只有意志坚强的人才能到达彼岸。这是伟大的马克思的名言名句，送予意志坚强的你，希望继续坚持，早日登上理想的彼岸，regrads.",

        "AAA": "Your pin code is 111111, please do not disclose it.",
        "BBB": "Your pin code is 111111, please do not disclose it, if you have any question, please contact me, as the M800 cannot provide service, Vietnam is left empty, so I do not pick up your phone call,  best regard.",
        "111": "Your pin code is 111111, please do not disclose it.",
        "222": "Your pin code is 111111, please do not disclose it, if you have any question, please contact me, as the M800 cannot provide service, Vietnam is left empty, so I do not pick up your phone call,  best regard.",
        "CCC": "您的注册验证码为：111111",
        "333": "您的验证码是111111。请注意保护您的验证码信息，不要分享给其他人。",
        "DDD": "您的一次性验证码为 111111 ,请勿告知他人,谢谢。[今日知识]知识就像海洋，只有意志坚强的人才能到达彼岸。这是伟大的马克思的名言名句，送予意志坚强的你，希望继续坚持，早日登上理想的彼岸，regrads.",
        "444": "您的一次性验证码为 111111 ,请勿告知他人,谢谢。[今日知识]知识就像海洋，只有意志坚强的人才能到达彼岸。这是伟大的马克思的名言名句，送予意志坚强的你，希望继续坚持，早日登上理想的彼岸，regrads.",

    }
    for paras, templ in zip(tests_Paras, templs.items()):
        phoneNumber = paras.get("phoneNumber")
        if phoneNumber:
            dest_msisdn = phoneNumber[len(str(countryCode)):]
        else:
            continue # 'phoneNumber': None, 'errorMessage': 'NETWORK_OFFLINE',

        if ttextEnd:
            sms_content = f'{templ[1]}{paras.get("testIdText")}'
        else:
            # sms_content = f'{paras.get("testIdText")}{8}, {templ[1]}'
            sms_content = f'{templ[1]}'
            sms_content = sms_content.replace('111111', paras.get("testIdText"))
        print(sms_content)

        if senderID:
            original_addr = senderID
        else:
            original_addr = templ[0]
        send_sms(sms_content, original_addr, dest_msisdn, countryCode, route_id, auth_key)
    print('test_SMS, sent.\n')


def test_with_TelQ(country_list, n_need=8, operator_need=None, senderID=None, ttextEnd=False,
                   route_id="ROUTE_TST_Notification",
                   tenant_name='CMIPB',
                   auth_key="cOUlfIimjcBgfxf5cNaiOVRjhQfJj1FIIj3FXGRJnwLVkkAe#jiT4n96f8#eCpKN3vvnauinWCqZK4WrpRGpAw=="):
    '''

    :param country_list: 测试方向列表，如['Taiwan', 'sdasa'], 需要对应 telQ
    :param n_need: 所需测试短信数量
    :param operator_need: 所需测试的运营商，默认随机
    :param senderID: 若有senderID注册要求，请填写senderID，没有特定要求可以填'CloudSMS'或None
    :param route_id:
    :param auth_key: 默认使用 CMIPB 租户
    :return:
    '''
    tstBeginTime = datetime.datetime.now()
    tstBeginTime = tstBeginTime.strftime("%Y-%m-%d %H:%M:%S")

    obtain_token_and_add()
    availNetworks, availNetworks_countryName, availNetworks_mcc = get_availNetworks()
    print(availNetworks)
    # print(availNetworks_countryName)
    # print(availNetworks_mcc)

    all_test_paras = []
    for country_need in country_list:
        countryCode = dict_countryCode[country_need]
        print(f'=== country_need:{country_need}, countryCode:{countryCode}')
        availNetworks_need = get_availNetworks_need(availNetworks_countryName, country_need, operator_need)
        json_data = gene_json_data(availNetworks_need, n_need)
        # json_data = {  # 有时候会用来测试某一个运营商
        #     "destinationNetworks": [
        #         {'mcc': '510',
        #          'countryName': 'Indonesia',
        #          'mnc': '10',
        #          'providerName': 'Telkomsel',
        #          'portedFromMnc': None,
        #          'portedFromProviderName': None},
        #     ],
        #
        # }
        tests_Paras = request_new_tests(json_data)
        # tests_Paras = [  # 有时候用来re-test，因为平台发送失败导致该资源申请了还没使用
        #     {'id': 11784345, 'testIdText': 'JNehmtvciZ', 'phoneNumber': '923212771948', 'errorMessage': None,
        #      'destinationNetwork': {'mcc': '410', 'mnc': '04', 'portedFromMnc': '07'}},
        #     {'id': 11784348, 'testIdText': 'XFphKfusLM', 'phoneNumber': '923313175374', 'errorMessage': None,
        #      'destinationNetwork': {'mcc': '410', 'mnc': '04', 'portedFromMnc': '03'}}]

        print("tests_Paras:", tests_Paras)
        send_test_Message(tests_Paras, countryCode, route_id, auth_key, senderID=senderID, ttextEnd=ttextEnd)
        update_telDB(json_data, tests_Paras)
        all_test_paras.extend(tests_Paras)

    # all_test_paras = []
    # for country_need, tests_Paras in zip(country_list, all_test_paras):
    #     countryCode = dict_countryCode[country_need]
    #     send_test_Message(tests_Paras, countryCode, route_id, auth_key)
    time.sleep(1)
    tstEndTime = datetime.datetime.now()
    tstEndTime = tstEndTime.strftime("%Y-%m-%d %H:%M:%S")

    for _ in range(3):
        time.sleep(20)
        show_test_results(all_test_paras)
        print('==' * 10)

    analy_dispatchingLog(tenant_name=tenant_name, start_date=tstBeginTime, end_date=tstEndTime)

    for paras in all_test_paras:
        print('{"id":', paras.get("id"), '},')

    print()
    eval_tests_paras(all_test_paras)
    return all_test_paras

def sendSMS_with_telQ(country_need, n_need=8, operator_need=None, senderID=None, ttextEnd=False,
                      route_id="ROUTE_TST_Notification",
                      auth_key="cOUlfIimjcBgfxf5cNaiOVRjhQfJj1FIIj3FXGRJnwLVkkAe#jiT4n96f8#eCpKN3vvnauinWCqZK4WrpRGpAw=="):
    '''
    :param country_need: 测试方向，如'Taiwan', 需要对应 telQ
    :param n_need: 所需测试短信数量
    :param operator_need: 所需测试的运营商
    :param senderID: 若有senderID注册要求，请填写senderID，没有特定要求可以填'CloudSMS'或None
    :param route_id:
    :param auth_key: 默认使用 CMIPB 租户
    :return:
    '''
    tstBeginTime = datetime.datetime.now()
    tstBeginTime = tstBeginTime.strftime("%Y-%m-%d %H:%M:%S")

    obtain_token_and_add()
    availNetworks, availNetworks_countryName, availNetworks_mcc = get_availNetworks()

    countryCode = dict_countryCode[country_need]
    print(f'=== country_need:{country_need}, countryCode:{countryCode}')
    availNetworks_need = get_availNetworks_need(availNetworks_countryName, country_need, operator_need)
    json_data = gene_json_data(availNetworks_need, n_need)
    tests_Paras = request_new_tests(json_data)

    print("tests_Paras:", tests_Paras)

    send_test_Message(tests_Paras, countryCode, route_id, auth_key, senderID=senderID, ttextEnd=ttextEnd)
    update_telDB(json_data, tests_Paras)

    time.sleep(5)
    # tstEndTime = tstBeginTime + datetime.timedelta(minutes=1)
    tstEndTime = datetime.datetime.now()
    tstEndTime = tstEndTime.strftime("%Y-%m-%d %H:%M:%S")
    return tests_Paras, tstBeginTime, tstEndTime

def get_SMS_result_both_telQ_and_CloudSMS(tests_Paras, tstBeginTime, tstEndTime, tenant_name='CMIPB'):
    phones_diff_rate = eval_tests_paras(tests_Paras)
    pRate = show_test_results(tests_Paras)
    sRate = analy_dispatchingLog(tenant_name=tenant_name, start_date=tstBeginTime, end_date=tstEndTime)
    print(f"pRate: {pRate}, sRate: {sRate}, rateDiff: {pRate-sRate}")
    return phones_diff_rate, pRate, sRate

def test_with_TelQ_1(country_list, n_need=1, operator_need=None, senderID=None, ttextEnd=False,
                   route_id="ROUTE_TST_Notification",
                   tenant_name='CMIPB',
                   auth_key="cOUlfIimjcBgfxf5cNaiOVRjhQfJj1FIIj3FXGRJnwLVkkAe#jiT4n96f8#eCpKN3vvnauinWCqZK4WrpRGpAw=="):
    '''
    该版本用于记录 路由质量测试结果， 耗时15分钟起
    :param country_list: 测试方向列表，如['Taiwan', 'sdasa'], 需要对应 telQ
    :param n_need: 所需测试短信数量
    :param operator_need: 所需测试的运营商
    :param senderID: 若有senderID注册要求，请填写senderID，没有特定要求可以填'CloudSMS'或None
    :param route_id:
    :param auth_key: 默认使用 CMIPB 租户
    :return:
    '''
    dire_rst = {}
    for country_need in country_list:
        tests_Paras, tstBeginTime, tstEndTime = sendSMS_with_telQ(country_need, n_need, operator_need, senderID, ttextEnd, route_id, auth_key)
        dire_rst[country_need] = {}
        dire_rst[country_need]["tests_Paras"] = tests_Paras
        dire_rst[country_need]["tstBeginTime"] = tstBeginTime
        dire_rst[country_need]["tstEndTime"] = tstEndTime
        dire_rst[country_need]["n_need"] = n_need

    for _ in range(3):
        time.sleep(20)
        for country_need in country_list:
            print('\n', datetime.datetime.now(), country_need)
            paras = dire_rst[country_need]
            phones_diff_rate, pRate, sRate = get_SMS_result_both_telQ_and_CloudSMS(paras["tests_Paras"], paras["tstBeginTime"], paras["tstEndTime"], tenant_name=tenant_name)
        print('==' * 10)
        if 1 == len(country_list) and 1 == pRate and 1 == sRate:
            break
    if 1 == len(country_list) and 1 == pRate and 1 == sRate:
        pass
    else:
        time.sleep(60 * 15)

    for country_need in country_list:
        paras = dire_rst[country_need]
        phones_diff_rate, pRate, sRate = get_SMS_result_both_telQ_and_CloudSMS(paras["tests_Paras"], paras["tstBeginTime"], paras["tstEndTime"], tenant_name=tenant_name)
        dire_rst[country_need]["phones_diff_rate"] = phones_diff_rate
        dire_rst[country_need]["pRate"] = pRate
        dire_rst[country_need]["sRate"] = sRate
    print(f'dire_rst: {dire_rst}')
    return dire_rst

def update_routeTST_pRate(supplier_name, supplier_id, uid, dire_rst):
    double_list = []
    columns = ['supplier_name', 'supplier_id', 'uid', 'dire',
               'tstBeginTime', 'tstEndTime', 'testAmt', 'phonesDiffRate',
               'pRate', 'sRate', 'rateDiff']
    for dire in dire_rst.keys():
        paras = dire_rst[dire]
        double_list.append([supplier_name, supplier_id, uid, dire,
                            paras["tstBeginTime"], paras["tstEndTime"], paras["n_need"], paras["phones_diff_rate"],
                            paras["pRate"], paras["sRate"], paras["pRate"]-paras["sRate"]])
    df = pd.DataFrame(double_list, columns=columns)
    df.to_csv(routeTST_pRate_path, header=False, index=False, mode='a')
    # df.to_csv(r'routeTST_pRate.csv', index=False, mode='a')
    print('=== routeTST_pRate.csv to_csv ===, done.')


if __name__ == '__main__':
    print('program begin...')
    # country_list = ['Hong Kong','Macau','Taiwan',]#'Singapore','Australia']
    # country_list = ['Switzerland','Haiti','Cuba','Panama','Mexico','Cambodia',
    #                 'Japan','Algeria','Austria','France','South Korea','Sweden',
    #                 'Netherlands','United States of America','Canada','Germany','Norway','Singapore','Hong Kong',
    #                 ]
    # country_list = ['Saudi Arabia',]
    # dires_need = ['Australia', 'Brazil', 'Canada', 'Colombia', 'Japan',
    #               'Mexico', 'Singapore', 'South Africa', 'South Korea', 'Taiwan',
    #               'United Kingdom', 'India', 'Indonesia', 'Vietnam',]
    # country_list = ['Russian Federation']
    # country_list = ['Pakistan', ]  # 'Marshall Islands',
    # country_list = ['India', ]  # 'Marshall Islands',
    # country_list = ['United States of America',]
    # country_list = ['United Arab Emirates',]
    # country_list = ['Turkey', 'United States', 'Canada', 'Australia', 'Singapore', 'Malaysia', 'Philippines', ]
    # country_list = ['United Arab Emirates', 'Qatar', 'Bahrain', 'Iraq', 'Egypt',]
    # country_list = ['Saudi Arabia',]
    country_list = [
        # 'South Korea',
        # 'Pakistan',
        # 'Indonesia',
        # 'Malaysia',
        # 'Republika Slovenija',
        'China',
        # 'Hong Kong',
        # 'Macau',
        # 'Taiwan',
        # 'Singapore',
        # 'Australia',
    ]

    # tenant_name = 'CMIPB_Tong'
    # auth_key = 'cOUlfIimjcBgfxf5cNaiOXmsfkipVsqAyo6qe0mCxGr5VZFOiB5XB8rMy+N#0AUyZrwWr9tTos6wEjuWEJHlNw=='

    tenant_name = 'CMIPB'
    auth_key = 'cOUlfIimjcBgfxf5cNaiOVRjhQfJj1FIIj3FXGRJnwLVkkAe#jiT4n96f8#eCpKN3vvnauinWCqZK4WrpRGpAw=='

    country_replace = {'United States': 'United States of America',
                       'Russia': 'Russian Federation',
                       'Republika Slovenija':'Slovenia',}
    country_list = [country_replace[x] if x in country_replace else x for x in country_list]

    ## 基于telQ的短信发送及结果，耗时至少2分钟
    # test_with_TelQ(country_list, tenant_name=tenant_name, auth_key=auth_key, n_need= 1, operator_need=None, route_id='RTST060_Notification_02', senderID=None)

    ## 路由质量测试，耗时至少15分钟。
    dire_rst = test_with_TelQ_1(country_list, tenant_name=tenant_name, auth_key=auth_key, n_need=10, operator_need=None, route_id='WT_Notification_47', senderID=None)
    update_routeTST_pRate(supplier_name='PT Cakra Alpha Spektrum - A2P Special  Route', supplier_id='11320', uid='14646', dire_rst=dire_rst)

    print('program done.')


