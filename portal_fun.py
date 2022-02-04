from portal_operation_uip_v2 import *

def update_postpaid_product_v2(old_product_name='ALIBABA_RTST_PACK003', new_product_name='ALIBABA_RTST_PACK004',
                               dps={'Thailand': 0.08, 'Australia': 0.09}):
    '''
        后付费产品更新：基于旧产品，创建新产品；有价格修改的，请填写dps字典；价格没修改的不用填，会保持不变
        该函数主要应对已有方向太多，需要复制太多价格的问题而产生的。
        # 产品的更新，通常在于
            # 方向变化：新增方向，删除方向
            # 价格变化:
        :param old_product_name:
        :param new_product_name:
        :param dps:
        :return:
    '''
    html = get_product_detail(old_product_name)
    channel_id = html['data']['channel_id']
    channel_list = html['data']['channel_list']

    channel_dict = {channel.get('region'): channel.get('sale_price') for channel in channel_list}  # 旧产品价格
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
            channel_unit['sale_price'] = channel_dict.get(channel_unit['region'])
        new_channel_list.append(channel_unit)
    data = {"product_name": new_product_name, "channel_id": channel_id, "pay_type": 2, "price_currency": "USD",
            "sale_price": 0, "total_num": 0, "use_valid_term": 0, "use_valid_term_unit": "月",
            "start_product_valid_term": "", "end_product_valid_term": "", "is_open": 2,
            "valid_time_type": 1, "channel_des": "undefined/undefined ()", "p2p_type": 2,
            "channel_list": new_channel_list}
    data = json.dumps(data)
    html = requests.post(url, data=data, headers=HEADERS_PORTAL)
    print(html.text)
    print(f'update_product done.\n')


#============ fun
def fun_update_add_business_channel():
    'update add 业务通道'
    dires_need = [
        "Colombia",
        "Brazil",
        "Peru",
        "Kenya",
        "Mexico",
        "Ghana",
        "Taiwan",
    ]
    businessChannel_modify_create_v2(business_Channel_Name='CXY_SMPP', dires_need=dires_need,
                                     LName=['JCCNCMI01', 'JCCNCMI02'])


def fun_update_postpaid_product():
    'update 创建产品'
    dps = {
        "Colombia": 0.0015,
        "Brazil": 0.0081,
        "Peru": 0.0763,
        "Kenya": 0.0885,
        "Mexico": 0.0152,
        "Ghana": 0.1051,
    }
    old_product_name = 'CXY_PACK06'
    new_product_name = 'CXY_PACK07'
    update_postpaid_product_v2(old_product_name, new_product_name, dps)


def fun_update_bussinessChannel_and_postpaid_product():
    'update add 业务通道，并update创建产品'
    dps = {
        "Colombia": 0.0015,
        "Brazil": 0.0081,
        "Peru": 0.0763,
        "Kenya": 0.0885,
        "Mexico": 0.0152,
        "Ghana": 0.1051,
    }
    dires_need = list(dps.keys())
    business_Channel_Name = 'CXY_SMPP'
    LName = ['JCCNCMI01', 'JCCNCMI02']
    old_product_name = 'CXY_PACK06'
    new_product_name = 'CXY_PACK07'
    businessChannel_modify_create_v2(business_Channel_Name, dires_need, LName)
    update_postpaid_product_v2(old_product_name, new_product_name, dps)

def fun_create_bChannel_and_product_and_order():
    '新建业务通道、创建产品及订购'
    LName = ['JNTKCMI01', 'JNTKCMI02']
    business_Name = 'RTST061'
    business_Channel_Name = f'{business_Name}_API'
    product_name = f'{business_Name}_PACK01'
    dires_need = [
        'Hong Kong',
        'Macau',
        'Taiwan',
    ]
    dps = {dire: 0.01 for dire in dires_need}
    businessChannel_create_v2(LName, business_Channel_Name, business_Name, dires_need)
    create_postpaid_product_v2(business_Channel_Name, product_name, dps)
    order_product(product_name, tenant_name='CMIPB', oder_derial_number=None)
    channel_id, channel_code, english_name, route_id = get_businessChannel_id(business_Channel_Name)
    print(route_id)


if __name__ == "__main__":
    print('program begin...')

    # 'update add 业务通道'
    # fun_update_add_business_channel()

    # 'update 创建产品'
    # fun_update_postpaid_product()

    # 'update add 业务通道，并update创建产品'
    # fun_update_bussinessChannel_and_postpaid_product()

    # '新建业务通道、创建产品及订购'
    fun_create_bChannel_and_product_and_order()
