import execjs
import time
import requests
import re
import json


def load_js_file(file_path):
    """加载并编译JS文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        script = file.read()
    return execjs.compile(script)


def get_sign(ctx, need_encrypt_str):
    """调用JS函数生成签名"""
    return ctx.call('i', need_encrypt_str)


def get_token(cookies):
    """从cookies中提取token"""
    return re.findall(r'_m_h5_tk=(.*?)_', cookies)[0]


def main(item_id):
    # 初始化JS环境
    ctx = load_js_file('mini-login-embedder-min.js')

    # 更换cookies
    cookies = "mtop_partitioned_detect=1; _m_h5_tk=aef3f9a4fd144db92c277c9ba8a5cf7a_1753809297439; _m_h5_tk_enc=06dfff4da0ab6102dc97cb836d29ccb1; cna=zMYPIU2guToCASIVWp8H3/9Z; xlly_s=1; cookie2=1e2a3186c15d8cfeda2f6942581ef961; tfstk=gxqmwnq7yruXjUC-yuiflyhkU_Q-cmisz5Kt6chNzblWMIKYQCVgaWevDleZs5V-N-KOh-pbPWeeDoQjXhmjfc5d9MIpl-isbksZr9cbU8MNex8llOOjfc5dwUKZlMm_gWv5p5yPEAH90APZQ8SrNATqbjuwaUkEacoZ7cuyzAMqQhoZuT2rNAoZ_5uVE0lSQvE24jU3uu5gVstiwjcUqx0mT-bBbhqkvqcU3bxNTuDcOXyqZh-ZtOxMg82AiHw-c8PnpSIymW28pog7j6jmluy3Vqq6IUw-RjmrGrCDVxVYIk0z0OpKguwaA4mh5Bh7f8zKRDR2uvmmi2r4wdWE0VkZ0jaAi3M0MRqnzoW9JYaaNlmxYMOq6ze3jAq11gV3eJEjPlfh4g86ze5TVhMPBu865qkSEXLzDXW6BpCeFTXk8DgqFx61ETY65qkSEXBlEePouYMfC"

    headers = {
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.goofish.com",
        "priority": "u=1, i",
        "referer": "https://www.goofish.com/",
        "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "cookie":cookies,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }

    token = get_token(cookies)
    print("token:", token)
    
    timestamp = int(time.time()) * 1000
    app_key = '34839810'

    request_data = {"itemId": item_id}
    sign = get_sign(ctx, f"{token}&{timestamp}&{app_key}&{json.dumps(request_data)}")
    print("sign:", sign)

    params = {
        "jsv": "2.7.2",
        "appKey": app_key,
        "t": timestamp,
        "sign": sign,
        "v": "1.0",
        "type": "originaljson",
        "accountSite": "xianyu",
        "dataType": "json",
        "timeout": "20000",
        "api": "mtop.taobao.idle.pc.detail",
        "sessionOption": "AutoLoginOnly",
        "spm_cnt": "a21ybx.item.0.0",
        "spm_pre": "a21ybx.im.head.1.77b93da6Hyz59j",
        "log_id": "77b93da6Hyz59j"
    }

    response = requests.post(
        url="https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/",
        headers=headers,
        params=params,
        data={"data": json.dumps(request_data)}
    )

    if response.status_code == 200:
        try:
            data = response.json().get('data')
            last_visit_time = data.get('sellerDO').get('lastVisitTime')
            print(last_visit_time)
        except Exception as e:
            print(response.json())
    else:
        print("Request failed with status code:", response.status_code)
        print(response.text)


if __name__ == '__main__':
    # https://www.goofish.com/item?id=946689965186
    main('946689965186')