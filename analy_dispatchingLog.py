import requests
import json
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
import datetime as dt
from portal_operation_uip_v2 import *

def get_dispatchingLog_DF(tenant_name="CMIPB", start_date=None, end_date=None, country_code=None, msisdn=None, uid=None, task_name=None):
    '''
    根据租户名，查询发送记录
    :param tenant_name: 租户名, 默认使用 CMIPB
    :param start_date: 如"2021-10-26 00:00:00",
    :param end_date: 如"2021-10-27 23:59:59",
    :param country_code: 比如 852
    :param msisdn: 手机号码，比如 62108888
    :param uid: CloudSMS使用的短信唯一id，如 5D221C3AC5471X0D26FA163EDF30CB
    :param task_name: 任务名称
    :return:
    '''

    if tenant_name == "CMIPB":
        tenant_id = 27
    elif tenant_name == 'BIGF':
        tenant_id = 5
    else:
        tenant_id = get_tenant_id(tenant_name)

    if start_date:
       pass
    else:
        start_date = str(datetime.combine(date.today() - timedelta(days=1), dt.time.min))
        end_date = str(datetime.combine(date.today(), dt.time.max))


    url = 'https://smsportal.jegotrip.com:8087/sms/stat/record'
    data = {"page": 1, "page_size": 10000, "start_date": start_date, "end_date": end_date,
            "tenement_id": tenant_id, "country_code": country_code, "msisdn": msisdn, "status": "",
            "task_name": task_name, "uid": uid}
    # "status": ""表示所有记录，另外有"Success", "Failed", "Unknown"
    # data = {"page": 1, "page_size": 10, "start_date": "2021-10-26 00:00:00", "end_date": "2021-10-27 23:59:59",
    #         "tenement_id": 27, "country_code": "213", "sendregions": 2, "msisdn": "2122121", "uid": "uiduid",
    #         "task_name": "mmn", "status": ""}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    html = json.loads(html.text)
    dispatching_Df = pd.DataFrame(html["data"]["data"])
    print(f'len of dispatchingLog_DF: {len(dispatching_Df)}')
    dispatching_Df.to_excel('cxy.xlsx')
    return dispatching_Df


def analy_dispatchingLog(tenant_name="CMIPB", start_date=None, end_date=None, country_code=None, msisdn=None, uid=None, task_name=None):
    dispatchingLog_DF = get_dispatchingLog_DF(tenant_name, start_date, end_date, country_code, msisdn, uid, task_name)
    print(f'{tenant_name}: From {start_date} To {end_date}: ')
    print(f'len of dispatchingLog_DF: {len(dispatchingLog_DF)}')
    gb1 = dispatchingLog_DF.groupby(["status", "report_code"]).size()
    gb2 = gb1 / len(dispatchingLog_DF)
    pdc = pd.concat([gb1, gb2], axis=1)
    pdc.columns = ['size', 'ratio']
    print(pdc)
    try:
        sRate = pdc['ratio'][('Success', 'DELIVERED')]
    except:
        sRate = 0
    finally:
        print(f'sRate: {sRate}')
        return sRate



if __name__ == "__main__":

    tenant_name = "CIK"
    start_date = '2021-09-01 00:00:00'
    end_date =   '2021-09-10 23:55:23'
    # start_date = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # 此时此刻
    # start_date = str(datetime.combine(date.today() - timedelta(days=1), dt.time.min)) # 前一天最小时间
    # start_date = str(datetime.combine(date.today(), dt.time.min))  # 当天最小时间
    # end_date = str(datetime.combine(date.today(), dt.time.max)) # 当天最大时间

    print(f'{tenant_name}: From {start_date} To {end_date}: ')
    analy_dispatchingLog(tenant_name, start_date, end_date, country_code=886)
    print('program done.')

    # #
    # dispatchingLog_DF['send_time'] = pd.to_datetime(dispatchingLog_DF['send_time'])
    # dispatchingLog_DF['report_date'] = pd.to_datetime(dispatchingLog_DF['report_date'])
    # # dispatchingLog_DF = dispatchingLog_DF.set_index('send_time')
    # dispatchingLog_DF = dispatchingLog_DF[['failure_cause', 'msisdn', 'proposal', 'report_code', 'report_date', 'route_id', 'send_time',
    #    'source_msisdn', 'status', ]]
    #
    # dispatchingLog_DF['report_date'] < pd.to_datetime('2021-11-08 16:13:18')
    #
    # from datetime import timedelta
    # min_time = dispatchingLog_DF['send_time'].min() # Timestamp('2021-11-08 14:52:03')
    # # dispatchingLog_DF[dispatchingLog_DF[]]
    # dt1 = pd.to_datetime('2021-11-08 16:12:57') + timedelta(seconds=5)
    # dt2 = pd.to_datetime('2021-11-08 16:12:50')
    # #
