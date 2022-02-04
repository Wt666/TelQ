import requests
import time
import json
import urllib3
urllib3.disable_warnings()
import traceback
import sys
# from email_netease import textMailer_send

url_base = {
    # "my_test_company": "https://172.22.223.192:1815/dave/io",  # STG的公司内网访问地址
    "my_prod_company": "https://172.22.223.96:1815/dave/io",  # prod的公司内网访问地址
    # "my_prod_company": "https://192.168.11.68:1815/dave/io",  # prod的公司服务器内网访问地址
    # "my_prod_company": "https://cloudsms-new.jegotrip.com.cn:1815/dave/io",  # API外部访问地址
}
url = url_base["my_prod_company"]

def send_alert_email(msg):
    to_addrs = [ 'tonghongpui@cmi.chinamobile.com'] # 'rexwang@cmi.chinamobile.com',
    subject = 'API 短信发送请求异常'
    content = f'具体信息如下：\n{msg}'
    textMailer_send(from_addr='CMIPB_Tong', to_addrs=to_addrs,
                    subject=subject, content=content)

def post_data(data):
    try:
        data = json.dumps(data)
        print("\nreq:{}".format(data))

        for _ in range(5):
            rsp = requests.post(url, data, verify=False)
            if rsp.status_code == 200:  # API请求正常
                return True, rsp
        # API请求异常
        return False, rsp
    except Exception as e:
        print(f'try except info: {e.args}')
        traceback.print_exc()
        info = sys.exc_info()
        print(info)
        return False, str(info)

# def post_and_resp(data):
#     try:
#         data = json.dumps(data)
#         print("\nreq:{}".format(data))
#
#         for _ in range(5):
#             rsp = requests.post(url, data, verify=False)
#             if rsp.status_code == 200:
#                 # API请求正常
#                 rsp_new = rsp.json()
#                 code = rsp_new["RESULT_CODE"]
#                 desc = rsp_new["RESULT_DESC"]
#                 if code == 1:
#                     print(f'API RESULT_DESC:{desc}, SMS_UID:{rsp_new["DETAIL_LIST"][0]["SMS_UID"]}')
#                     return True, rsp_new["DETAIL_LIST"][0]['SMS_UID']
#                 else:
#                     msg = f"API 响应正常，发送异常: RESULT_CODE: {code}, RESULT_DESC: {desc}, \nrsp:{rsp_new}"
#                     print(msg)
#                     return False, msg
#         # API请求异常
#         print(f'API 响应异常： rsp.status_code: {rsp.status_code}')
#         print(f'rsp.text: {rsp.text}')
#         return False, rsp.text
#     except Exception as e:
#         print(f'try except info: {e.args}')
#         traceback.print_exc()
#         info = sys.exc_info()
#         print(info)
#         return False, info

def send_sms(sms_content, original_addr, dest_msisdn, country_code, route_id, auth_key):
    # if original_addr in ['whatsapp', 'facebook']:
    #     signature = None
    # else:
    #     signature = original_addr
    '''
    单独发送一条短信
    :param sms_content: 短信内容
    :param original_addr: 也称OA或SenderID
    :param dest_msisdn: 目标手机号码（不含区号）
    :param country_code: 目标手机号码区号
    :param route_id: CloudSMS业务通道，由CloudSMS管理人员配置具体策略生成。
    :param auth_key: CloudSMS租户识别码，由CloudSMS管理人员配置具体策略生成。
    :return:
    '''
    try:
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {
            "METHOD": "SMS_SEND_REQUEST",
            "TYPE": "REQUEST",
            "SERIAL": 1,
            "TIME": local_time,
            "AUTH_KEY": auth_key, # 租户的AUTH_KEY
            "ROUTE_ID": route_id,  # 业务通道Route_id
            "PRIORITY": 0,
            # "SIGNATURE": signature,
            # "SIGNATURE_TYPE": 3,
            "VERSION": "2021-01-01",
            "SMS_CONTENT": sms_content,
            "ORIGINAL_ADDR": original_addr,
            "MULTI_MSISDN_LIST": [{"DEST_MSISDN": str(dest_msisdn),
                                   "COUNTRY_CODE": int(country_code)}],
        }

        rspFlag, rsp = post_data(data)
        if rspFlag:
            rsp_json = rsp.json()
            code = rsp_json["RESULT_CODE"]
            desc = rsp_json["RESULT_DESC"]
            if code == 1:
                print(f"API 响应正常: RESULT_DESC: {desc}")
                print(f'SMS_UID: {rsp_json["DETAIL_LIST"][0]["SMS_UID"]}')  # 如果是批量的，可遍历列表
                return rsp_json
            else:
                msg = f"API 响应正常，发送提交失败: RESULT_CODE {code}, RESULT_DESC:{desc}, \nrsp:{rsp_json}"
                print(msg)
                send_alert_email(msg)
                return None
        else:
            if isinstance(rsp, str):
                print(f'程序异常, {rsp}')
                send_alert_email(rsp)
            else:
                print(f'API 响应异常, 发送提交失败: rsp.status_code: {rsp.status_code}')
                print(f'rsp.text: {rsp.text}')
                send_alert_email(rsp.text)
            return None
    except Exception as e:
        print(f'try except info: {e.args}')
        traceback.print_exc()
        info = sys.exc_info()
        print(info)
        return None

def send_sms_mini_batch(sms_content, original_addr, dest_msisdns, country_codes, route_id, auth_key):
    '''
    单独发送一小批短信，短信内容唯一
    批次量限制多大，请咨询CloudSMS人员
    唯一区别是：调用该接口，只需post一次数据，就可以发送一批短信。
    :param sms_content: 短信内容
    :param original_addr: 也称OA或SenderID
    :param dest_msisdns: 目标手机号码（不含区号）, 如 [67657441,62107007]
    :param country_codes: 目标手机号码区号， 如 [852, 852]
    :param route_id: CloudSMS业务通道，由CloudSMS管理人员配置具体策略生成。
    :param auth_key: CloudSMS租户识别码，由CloudSMS管理人员配置具体策略生成。
    :return:
    '''
    try:
        multi_msisdn_list = []
        for da, country_code in zip(dest_msisdns, country_codes):
            multi_msisdn_list.append({"DEST_MSISDN": str(da), "COUNTRY_CODE": int(country_code)})

        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        data = {
            "METHOD": "SMS_SEND_REQUEST",
            "TYPE": "REQUEST",
            "SERIAL": 1,
            "TIME": local_time,
            "AUTH_KEY": auth_key, # 租户的AUTH_KEY
            "ROUTE_ID": route_id,  # 业务通道Route_id
            "PRIORITY": 0,
            # "SIGNATURE": tem,
            # "SIGNATURE_TYPE": 1,
            "VERSION": "2021-01-01",
            "SMS_CONTENT": sms_content,
            "ORIGINAL_ADDR": original_addr,
            "MULTI_MSISDN_LIST": multi_msisdn_list,
        }

        rspFlag, rsp = post_data(data)
        if rspFlag:
            rsp_json = rsp.json()
            code = rsp_json["RESULT_CODE"]
            desc = rsp_json["RESULT_DESC"]
            if code == 1:
                print(f"API 响应正常: RESULT_DESC: {desc}")
                # print(f'SMS_UID: {rsp_json["DETAIL_LIST"][0]["SMS_UID"]}')  # 如果是批量的，可遍历列表
                for detail in rsp_json["DETAIL_LIST"]:
                    print(f'SMS_UID: {detail["SMS_UID"]}')
                return rsp_json
            else:
                msg = f"API 响应正常，发送提交失败: RESULT_CODE {code}, RESULT_DESC:{desc}, \nrsp:{rsp_json}"
                print(msg)
                send_alert_email(msg)
                return None
        else:
            if isinstance(rsp, str):
                print(f'程序异常, {rsp}')
                send_alert_email(rsp)
            else:
                print(f'API 响应异常, 发送提交失败: rsp.status_code: {rsp.status_code}')
                print(f'rsp.text: {rsp.text}')
                send_alert_email(rsp.text)
            return None
    except Exception as e:
        print(f'try except info: {e.args}')
        traceback.print_exc()
        info = sys.exc_info()
        print(info)
        return None


if __name__ == "__main__":
    original_addr = 'CloudSMS'
    sms_content = "您的注册验证码为：112233"
    route_id = "ROUTE_TST_Notification"  # CloudSMS业务通道
    auth_key = "cOUlfIimjcBgfxf5cNaiOVRjhQfJj1FIIj3FXGRJnwLVkkAe#jiT4n96f8#eCpKN3vvnauinWCqZK4WrpRGpAw=="  # CloudSMS租户的AUTH_KEY

    # # 单独发送一条短信
    # country_code = 852
    # dest_msisdn = 62107007
    # send_sms(sms_content, original_addr, dest_msisdn, country_code, route_id, auth_key)

    # 单独发送一批短信，短信内容唯一
    # 批次量限制多大，请咨询CloudSMS人员
    country_code = [852]*400
    dest_msisdn = [62107007]*400
    send_sms_mini_batch(sms_content, original_addr, dest_msisdn, country_code, route_id, auth_key)



