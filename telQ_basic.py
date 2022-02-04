import numpy as np
import pandas as pd
import requests
import time
import json
import random
import urllib3

urllib3.disable_warnings()
# import io
# import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf8') #改变标准输出的默认编码


# We can use the TelQ Telecom REST API to obtain a list with their available networks, Request tests and consult test results.
# TelQ API Introduction: https://api-doc.telqtele.com/#new-telq-telecom-java-sdk
API_VERSION = "v2.1"
APPID = 9851
APPKEY = '&OZFpE1t3g7CC+WmttubLSQcdM@($zeZ5P9'
HEADERS_TELQ = {
    "Content-Type": "application/json",
    'accept': "*/*",
    # 'authority': 'api.telqtele.com',
}
# telDB_path = r'telDB.csv' # 构建telQ号码库
telDB_path = r'P:\telDB.csv' # 保存在公共盘
# 从portal数据生成
dict_countryCode = {'Eritrea': 291, 'Kosovo': 383, 'Slovenia': 386, 'Afghanistan': 93, 'Albania': 355,
                    'Algeria': 213, 'Andorra': 376, 'Angola': 244, 'Anguilla': 1264, 'Antigua and Barbuda': 1268,
                    'Argentina': 54, 'Armenia': 374, 'Aruba': 297, 'Australia': 61, 'Austria': 43, 'Azerbaijan': 994,
                    'Bahamas': 1242, 'Bahrain': 973, 'Bangladesh': 880, 'Barbados': 1246, 'Belarus': 375, 'Belgium': 32,
                    'Belize': 501, 'Benin': 229, 'Bermuda': 1441, 'Bhutan': 975, 'Bolivia': 591,
                    'Bosnia and Herzegovina': 387, 'Botswana': 267, 'Brazil': 55, 'British Virgin Islands': 284,
                    'Brunei': 673, 'Bulgaria': 359, 'Burkina Faso': 226, 'Burundi': 257, 'Cambodia': 855,
                    'Cameroon': 237, 'Canada': 1, 'Cape Verde': 238, 'Cayman Islands': 1345,
                    'Central African Republic': 236, 'Chad': 235, 'Chile': 56, 'China': 86, 'Colombia': 57,
                    'Comoros': 269, 'Cook Islands': 682, 'Costa Rica': 506, "Cote d'Ivoire": 225, 'Croatia': 385,
                    'Cuba': 53, 'Cyprus': 357, 'Czech Republic': 420, 'Democratic Republic Of The Congo': 243,
                    'Republic of the Congo': 242, 'Denmark': 45, 'Djibouti': 253, 'Dominican Republic': 1809,
                    'East Timor': 670, 'Ecuador': 593, 'Egypt': 20, 'El Salvador': 503, 'Equatorial Guinea': 240,
                    'Estonia': 372, 'Ethiopia': 251, 'Falkland Islands': 500, 'Faroe Islands': 298, 'Fiji': 679,
                    'Finland': 358, 'France': 33, 'French Guiana': 594, 'French Polynesia': 689, 'Gabon': 241,
                    'Gambia': 220, 'Georgia': 995, 'Germany': 49, 'Ghana': 233, 'Gibraltar': 350, 'Greece': 30,
                    'Greenland': 299, 'Grenada': 1473, 'Guadeloupe': 590, 'Guam': 1671, 'Guatemala': 502, 'Guinea': 224,
                    'Guinea-Bissau': 245, 'Guyana': 592, 'Haiti': 509, 'Honduras': 504, 'Hong Kong': 852, 'Hungary': 36,
                    'Iceland': 354, 'India': 91, 'Indonesia': 62, 'Iran': 98, 'Iraq': 964, 'Ireland': 353,
                    'Israel': 972, 'Italy': 39, 'Jamaica': 1876, 'Japan': 81, 'Jordan': 962, 'Kazakhstan': 7,
                    'Kenya': 254, 'Kiribati': 686, 'North Korea': 850, 'Kuwait': 965, 'Kyrgyzstan': 996, 'Laos': 856,
                    'Latvia': 371, 'Lebanon': 961, 'Lesotho': 266, 'Liberia': 231, 'Libya': 218, 'Liechtenstein': 423,
                    'Lithuania': 370, 'Luxembourg': 352, 'Macau': 853, 'Macedonia': 389, 'Madagascar': 261,
                    'Malawi': 265, 'Malaysia': 60, 'Maldives': 960, 'Mali': 223, 'Malta': 356, 'Marshall Islands': 692,
                    'Martinique': 596, 'Mauritania': 222, 'Mauritius': 230, 'Mayotte': 269, 'Mexico': 52,
                    'Micronesia': 691, 'Moldova': 373, 'Monaco': 377, 'Mongolia': 976, 'Montenegro': 382,
                    'Montserrat': 1664, 'Morocco': 212, 'Mozambique': 258, 'Myanmar': 95, 'Namibia': 264, 'Nauru': 674,
                    'Nepal': 977, 'Netherlands': 31, 'Netherlands Antilles': 599, 'New Caledonia': 687,
                    'New Zealand': 64, 'Nicaragua': 505, 'Niger': 227, 'Nigeria': 234, 'Niue': 683,
                    'Norfolk Island': 6723, 'Northern Mariana Islands': 1670, 'Norway': 47, 'Oman': 968, 'Pakistan': 92,
                    'Palau': 680, 'Palestine': 970, 'Panama': 507, 'Papua New Guinea': 675, 'Paraguay': 595, 'Peru': 51,
                    'Philippines': 63, 'Poland': 48, 'Portugal': 351, 'Puerto Rico': 1787, 'Qatar': 974, 'Reunion': 262,
                    'Romania': 40, 'Russian Federation': 7, 'Rwanda': 250, 'Saint Kitts and Nevis': 1869, 'Saint Lucia': 1758,
                    'Saint Martin': 590, 'Saint Pierre and Miquelon': 508, 'Saint Vincent and the Grenadines': 1784,
                    'Samoa': 685, 'San Marino': 378, 'Sao Tome and Principe': 239, 'Saudi Arabia': 966, 'Senegal': 221,
                    'Serbia': 381, 'Seychelles': 248, 'Sierra Leone': 232, 'Singapore': 65, 'Slovakia': 421,
                    'Solomon Islands': 677, 'Somalia': 252, 'South Africa': 27, 'South Korea': 82, 'South Sudan': 211,
                    'Spain': 34, 'Sri Lanka': 94, 'Sudan': 249, 'Suriname': 597, 'Swaziland': 268, 'Sweden': 46,
                    'Switzerland': 41, 'Syria': 963, 'Taiwan': 886, 'Tajikistan': 992, 'Tanzania': 255, 'Thailand': 66,
                    'Togo': 228, 'Tonga': 676, 'Trinidad and Tobago': 1868, 'Tunisia': 216, 'Turkey': 90,
                    'Turkmenistan': 993, 'Turks and Caicos Islands': 1649, 'Tuvalu': 688, 'Uganda': 256, 'Ukraine': 380,
                    'United Arab Emirates': 971, 'United Kingdom': 44, 'United States of America': 1, 'Uruguay': 598,
                    'Uzbekistan': 998, 'Vanuatu': 678, 'Vatican': 379, 'Venezuela': 58, 'Vietnam': 84,
                    'Wallis And Futuna': 681, 'Yemen': 967, 'Zambia': 260, 'Zimbabwe': 263}


def obtain_token_and_add():
    # === obtain the Token
    # Obtain the Token using the appId and appKey through the /token REST endpoint.
    # The TTL (Time to live) of the token is 86400 seconds (24 hours), hence the new token has to be re-created upon the expiration.
    url = f'https://api.telqtele.com/{API_VERSION}/client/token'
    data = json.dumps({'appId': APPID, 'appKey': APPKEY})
    rsp = requests.post(url, data=data, headers=HEADERS_TELQ)
    print(rsp)
    # print(rsp.text)
    # result
    # {"ttl":86400,"value":"ZXlKMGVYQWlPaUpLVjFRaUxDSmhiR2NpT2lKdWIyNWxJbjAuZXlKcFlYUWlPakUyTWpreE9URTFPRFVzSW01aVppSTZNVFl5T1RFNU1UWTBOU3dpWlhod0lqb3hOakk1TWpjM09UZzFMQ0prWVhSaElqb2lPRGt6WVRobFlqUXRNREJpTXkwME9XRTNMV0U1T1dRdE5qY3paR1ZtWkRNNE1tTmlMV05zYVdWdWRDSjku"}

    # add Token as the Authorization header
    token = json.loads(rsp.text)  # str to dict
    HEADERS_TELQ['Authorization'] = f'Bearer {token["value"]}'


def get_availNetworks():
    # get Available Networks
    # obtain_token_and_add() first.
    # This endpoint retrieves a list with all our currently available Networks.
    # The returned values (mcc, mnc, portedFromMnc) will be used in the /tests endpoint to request test numbers.
    # Test messages should then be sent from your system to these numbers to perform the test.
    url = f'https://api.telqtele.com/{API_VERSION}/client/networks'
    rsp = requests.get(url, headers=HEADERS_TELQ)
    print(rsp.text)
    availNetworks = eval(rsp.text.replace('null', "None"))
    print(f'len of list availNetworks: {len(availNetworks)}')

    ''' Inconsistency between mcc and country name:
        425: {'Israel', 'Palestine'}
        India: {'404', '405'}
        United States of America: {'310', '311'}
        '''
    availNetworks_mcc = {}
    availNetworks_countryName = {}
    for availNetwork in availNetworks:
        if availNetworks_mcc.get(availNetwork.get('mcc')):
            availNetworks_mcc[availNetwork.get('mcc')].append(availNetwork)
        else:
            availNetworks_mcc[availNetwork.get('mcc')] = [availNetwork]

        if availNetworks_countryName.get(availNetwork.get('countryName')):
            availNetworks_countryName[availNetwork.get('countryName')].append(availNetwork)
        else:
            availNetworks_countryName[availNetwork.get('countryName')] = [availNetwork]
    print(f'len of availNetworks_mcc: {len(availNetworks_mcc)}')
    print(f'len of availNetworks_countryName: {len(availNetworks_countryName)}')

    return availNetworks, availNetworks_countryName, availNetworks_mcc


def request_new_tests(json_data):
    # send tests request to telQ, to obtain testID、testIdText、phoneNumber, etc.

    url = f'https://api.telqtele.com/{API_VERSION}/client/tests'
    data = json.dumps(json_data)

    '''
    If you would like to authenticate telQ Test Results Callbacks, you can send an authentication token in this parameter.
    It will be included as the Authorization bearer token of the callbacks we make to your server.
    The callback URL where you would like to receive TestResult updates anytime your tests status changes.
    You can alse consult test results through the /results endpoint.
    '''
    # headers["results-callback-token"] = 'if needs,pleaes replace this str with your callback URL'

    rsp = requests.post(url, data=data, headers=HEADERS_TELQ)
    tests_Paras = eval(rsp.text.replace('null', "None"))
    # for paras in tests_Paras:
    #     print(paras)
    return tests_Paras

    # json_data = {
    #     "destinationNetworks":[
    #         {'mcc': '505', 'countryName': 'Australia', 'mnc': '19', 'providerName': 'Lycamobile (MVNO)',
    #          'portedFromMnc': None, 'portedFromProviderName': None},
    #         {'mcc': '505', 'countryName': 'Australia', 'mnc': '02', 'providerName': 'Optus', 'portedFromMnc': None,
    #          'portedFromProviderName': None},
    #         {'mcc': '505', 'countryName': 'Australia', 'mnc': '02', 'providerName': 'Optus', 'portedFromMnc': '19',
    #          'portedFromProviderName': 'Lycamobile (MVNO)'},
    #         {'mcc': '505', 'countryName': 'Australia', 'mnc': '02', 'providerName': 'Optus', 'portedFromMnc': '01',
    #          'portedFromProviderName': 'Telstra'},
    #     ],
    # }

    # return:
    # tests_Paras = [{"id": 11167325, "testIdText": "kqPwLmrdRW", "phoneNumber": "61470650180", "errorMessage": None,
    #   "destinationNetwork": {"mcc": "505", "mnc": "19", "portedFromMnc": None}},
    #  {"id": 11167326, "testIdText": "AnKwQOnVJD", "phoneNumber": "61402183593", "errorMessage": None,
    #   "destinationNetwork": {"mcc": "505", "mnc": "02", "portedFromMnc": None}},
    #  {"id": 11167327, "testIdText": "eOWwbvlePx", "phoneNumber": "61469764971", "errorMessage": None,
    #   "destinationNetwork": {"mcc": "505", "mnc": "02", "portedFromMnc": "19"}},
    #  {"id": 11167328, "testIdText": "ODZwABvEPD", "phoneNumber": "61467366880", "errorMessage": None,
    #   "destinationNetwork": {"mcc": "505", "mnc": "02", "portedFromMnc": "01"}}]


def get_test_result(testId):
    url = f'https://api.telqtele.com/{API_VERSION}/client/results/{testId}'
    rsp = requests.get(url, headers=HEADERS_TELQ)
    test_rst = json.loads(rsp.text)
    print(test_rst)
    return test_rst

    # testCreatedAt: Timestamp for when the test request was created in UTC using the ISO 8601 standard (e.g., 2020-02-13T17:05:27Z)
    # smsReceivedAt: Timestamp for when our backend receives notification from our test app that the test sms was received in the phone.
    # receiptDelay: (second) smsReceivedAt - testCreatedAt

    ## important param:  testStatus, senderDelivered, textDelivered,
    # rsp = {"id": 11167325, "testIdText": "kqPwLmrdRW", "senderDelivered": "CloudSMS",
    #        "textDelivered": "kqPwLmrdRW, your testID is 11167325, keep.", "testCreatedAt": "2021-09-16T08:18:12Z",
    #        "smsReceivedAt": "2021-09-16T09:03:10Z", "receiptDelay": 2698, "testStatus": "POSITIVE",
    #        "destinationNetworkDetails": {"mcc": "505", "mnc": "19", "portedFromMnc": null, "countryName": "Australia",
    #                                      "providerName": "Lycamobile (MVNO)", "portedFromProviderName": null},
    #        "smscInfo": {"smscNumber": "61469000111", "countryName": "Australia", "countryCode": "AU", "mcc": "505",
    #                     "mnc": "19", "providerName": "Lycamobile (MVNO)"}, "pdusDelivered": [
    #         "07911664090011F1040ED043F6BB4E9E36A70000129061913080042AEB38F4CE6CCBC9D22B0B947FD7E5207A794E4F1241E93928168BD96E33598D055A97CB7017"]}

    # test results:
    # {"id":11275375,"testIdText":"JlgwoDxLAJ","senderDelivered":null,"textDelivered":null,"testCreatedAt":"2021-09-29T02:09:24Z","smsReceivedAt":null,"receiptDelay":null,"testStatus":"WAIT","destinationNetworkDetails":{"mcc":"525","mnc":"05","portedFromMnc":"03","countryName":"Singapore","providerName":"StarHub","portedFromProviderName":"M1"},"smscInfo":null,"pdusDelivered":[]}
    # testStatus: WAIT ==============================


def show_test_results(tests_Paras):
    # Using the /results endpoint while providing the testId returned by the /tests endpoint response.
    t_len = len(tests_Paras)
    p_sum = 0
    status = {
        'WAIT': '=' * 30,
        'TEST_NUMBER_NOT_AVAILABLE': '=' * 30,
        'POSITIVE': '',
        'NOT_DELIVERED': '=' * 10,
        'TEST_NUMBER_OFFLINE': '=' * 10,
        'NETWORK_OFFLINE': '=' * 10,
        'INTERNAL_ERROR': '=' * 10,
    }
    res_dict = {}
    print('\ntest results: ')
    for paras in tests_Paras:
        testId = paras.get("id")
        test_rst = get_test_result(testId)
        if test_rst['testStatus'] == 'POSITIVE':
            p_sum += 1
        print(f'testStatus: {test_rst["testStatus"]} {status.get(test_rst["testStatus"])}')
        print(f'receiptDelay: {test_rst["receiptDelay"]}')
        res_dict[test_rst.get('id')] = test_rst.get('testStatus')
    res_df = pd.DataFrame.from_dict(res_dict, orient='index', columns=['testStatus'])
    res_df = res_df.reset_index().rename(columns={'index': 'id'})

    gb1 = res_df.groupby("testStatus").size()
    gb2 = gb1 / len(res_df)
    pdc = pd.concat([gb1, gb2], axis=1)
    pdc.columns = ['size', 'ratio']
    print(pdc)
    pRate = p_sum / t_len
    return pRate


def get_test_pRate(tests_Paras):
    print('tests_result:')
    t_len = len(tests_Paras)
    p_sum = 0
    for paras in tests_Paras:
        testId = paras.get("id")
        test_rst = get_test_result(testId)
        if test_rst['testStatus'] == 'POSITIVE':
            p_sum += 1
        elif test_rst['testStatus'] == 'NETWORK_OFFLINE':
            return -1
    pRate = p_sum / t_len
    return pRate


def gene_json_data(availNetworks_need, n_need=8):
    ## [{}, {}, ...]
    len_need = len(availNetworks_need)
    print(f"len of availNetworks_need: {len_need}")
    if n_need < len_need:
        print(f'more than {n_need} availNetworks, random {n_need} samples for test')
        json_data = {"destinationNetworks": random.sample(availNetworks_need, n_need)}
    else:
        print(f'less than {n_need + 1} availNetworks, arange {n_need} samples for test')
        availNetworks_need = availNetworks_need * n_need
        json_data = {"destinationNetworks": availNetworks_need[:n_need]}
    json_data['testIdTextType'] = 'NUMERIC'  # [ALPHA,ALPHA_NUMERIC,NUMERIC,WHATSAPP_CODE]
    # json_data['testIdTextCase'] = 'UPPER' # [UPPER,LOWER,MIXED]
    json_data['testIdTextLength'] = 6  # default=10,4-20
    # json_data['testTimeToLiveInSeconds'] = 3600 # The maximum amount of time you want your tests to wait for a message. Default is 1 hour. (Minimum of 1 minute, maximum of 3 hours)
    return json_data


def get_availNetworks_need(availNetworks_countryName, country_need, operator_need=None):
    availNetworks_need = []
    availNetworks_country_need = availNetworks_countryName.get(country_need)
    if operator_need:
        for aNetwork_dict in availNetworks_country_need:
            if aNetwork_dict['providerName'] == operator_need:
                availNetworks_need.append(aNetwork_dict)
    else:
        availNetworks_need = availNetworks_country_need
    return availNetworks_need


def update_telDB(json_data, tests_Paras):
    double_list = []
    columns = ["mcc", "mnc", "providerName", "portedFromMnc", "portedFromProviderName",
               "phoneNumber", "countryName", "countryCode", "telNumber", 'testID', 'testIdText']
    for dn, tp in zip(json_data["destinationNetworks"], tests_Paras):
        mcc, mnc, providerName, countryName = dn['mcc'], dn['mnc'], dn['providerName'], dn['countryName']
        portedFromMnc, portedFromProviderName = dn['portedFromMnc'], dn['portedFromProviderName']
        phoneNumber, testID, testIdText, = tp['phoneNumber'], tp['id'], tp['testIdText'],
        countryCode = dict_countryCode[countryName]
        telNumber = phoneNumber[len(str(countryCode)):]
        double_list.append([mcc, mnc, providerName, portedFromMnc, portedFromProviderName,
                            phoneNumber, countryName, countryCode, telNumber, testID, testIdText, ])
    df = pd.DataFrame(double_list, columns=columns, dtype=str)
    df.to_csv(telDB_path, header=False, index=False, mode='a')
    print('=== to_csv ===, done.')


def eval_tests_paras(tests_Paras):
    phone_list = []
    for paras in tests_Paras:
        print(paras.get("phoneNumber"))
        phone_list.append(paras.get("phoneNumber"))
    # print(f'len of phone_list: {len(phone_list)}')
    # print(f'len of phone_list set: {len(set(phone_list))}')
    phones_diff_rate = len(set(phone_list)) / len(phone_list)
    print(f'phones_diff_rate: {len(set(phone_list))}/{len(phone_list)} = {phones_diff_rate}')
    return phones_diff_rate


if __name__ == '__main__':
    print('program begin...')
    country = 'Hong Kong'
    # country = 'Macau'
    obtain_token_and_add()
    availNetworks, availNetworks_countryName, availNetworks_mcc = get_availNetworks()
    availNetworks_need = get_availNetworks_need(availNetworks_countryName, country, operator_need=None)
    json_data = gene_json_data(availNetworks_need, n_need=1)
    tests_Paras = request_new_tests(json_data)
    update_telDB(json_data, tests_Paras)

    print(json_data)
    print(tests_Paras)

    # show_test_results(tests_Paras)
    print('program done.')
