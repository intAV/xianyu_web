import execjs
import time
import requests
import re
import json


with open('mini-login-embedder-min.js','r') as file:
    script = file.read()

ctx = execjs.compile(script)

def get_sign(need_encrypt_str):
    sign = ctx.call('i',need_encrypt_str)
    return sign

def main():

    cookies = "mtop_partitioned_detect=1; _m_h5_tk=f4e77a1ac5f1db1a18f7b95301494285_1733264052365; _m_h5_tk_enc=6826514460d8b488caeee61968b19e04; cna=jE3WH6XpHhECASeCT0NxzZEV; xlly_s=1; XSRF-TOKEN=c9466113-eb0a-419f-9b5a-6fde48cb4d18; _samesite_flag_=true; cookie2=1898f2f6fa5fa03502a8a625a61d7e73; t=236e7fb4d4d7fd829f96994a47bf5a8a; _tb_token_=e3e5311e33773; arms_uid=85e7a82a-e891-4ed4-9e16-d5c9a1c37d6f; _uab_collina=173325506008891551970426; _bl_uid=gem5w430851v42bjw7pRu4bhyda0; x5sec=7b22733b32223a2266393939316432366131383437343730222c22617365727665723b33223a22307c434a572f76626f47454e32302f6154362f2f2f2f2f774577744954703041593d227d; isg=BDQ0cN3Y7ygrs3vkIRGnVWVkBfKmDVj3hWwaac6VX79COdGD6Bwohr41vXHhwZBP; tfstk=f4r-HoN5jsfu3rJvke_mtyuIoGXm9kePM7y6xXckRSFYLWKkqDmoRvGY_bclLzcBpjFEZ4m7EMULZronZu4uJrFzC4VLLTkIOWNKtzbcj8yrYD1gJGjgU-tF9MF-RYTfdvMsObp7ikyrYD100_LIu8P_0TkTVD6xcvHeRDMINtnjKAmBV2tWlIGqGXiIPHMjlYD9NXTSOtejgviIObkOkXWS9HUHYbmwPi1kV3Zxh6kueMtKnuM-vfw72HtIeY3-18GA_QghZqwEJkJev2277Wk_NQ1izJaYMYndmUi_HyNt3usMwxzuhWlbBpKLU0hbTYm9dgwx2b3_2SvBf5wYdP0YmOsZ20G7-0yHB_2Y272zDJvBl0nukVE-fGRStr2TvvEFTiFTQoPxh5sdNglbjl3q4CctKUBAHe8EPxl3Uuu8QbGZFxhGnYYe8q22xUhk3eTC0QDxstC98eu5e"

    headers = {
        "accept": "application/json",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded",
        "origin": "https://www.goofish.com",
        "priority": "u=1, i",
        "referer": "https://www.goofish.com/",
        "cookie":cookies,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36 Edg/131.0.0.0"
    }

    #cookie _m_h5_tk值 去掉时间戳
    token = re.findall(r'_m_h5_tk=(.*?)_',cookies)[0]
    # print(token)
    
    #当前时间戳
    j = int(time.time()) * 1000

    #appkey
    h = '34839810'

    #查询参数
    data = '{"itemId":"858419823538"}'

    need_encrypt_str = token + "&" + str(j) + "&" + h + "&" + data
    # print(need_encrypt_str)

    sign = get_sign(need_encrypt_str)

    url = "https://h5api.m.goofish.com/h5/mtop.taobao.idle.pc.detail/1.0/"
    params = {
        "jsv": "2.7.2",
        "appKey": "34839810",
        "t": j,
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
    data = {
        "data": "{\"itemId\":\"858419823538\"}"
    }
    response = requests.post(url, headers=headers, params=params, data=data)

    if response.status_code == 200:
        try:
            data = response.json().get('data')
            lastVisitTime = data.get('sellerDO').get('lastVisitTime')
            print(lastVisitTime)
        except Exception as e:
            print(e)
            print(response.json())
    else:
        print(response)



if __name__ == '__main__':
    main()