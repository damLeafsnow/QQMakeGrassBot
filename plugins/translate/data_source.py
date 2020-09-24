import hashlib
import json
import random
import requests


url = "http://api.fanyi.baidu.com/api/trans/vip/translate"
salt = random.randint(32768, 65536)


def translate(text, fromLang='zh', toLang='en'):
    # 从文件读取api账号
    # print(text)
    account = []
    try:
        with open('./datas/BAIDU_API', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line).strip()  # 清理/n和空格
                account.append(str_t)
            f.close()
            # print(account)
    except Exception as err:
        print(err)
    appid = account[0]
    secretKey = account[1]

# 生成签名
    sign = appid + text + str(salt) + secretKey
    sign = hashlib.md5(sign.encode()).hexdigest()
# post请求参数
    data = {
        "appid": appid,
        "q": text,
        "from": fromLang,
        "to": toLang,
        "salt": str(salt),
        "sign": sign,
    }
# post请求
    res = requests.post(url, data=data)
    json_result = json.loads(res.content)
    print(json_result)
# 输入信息错误
    if('error_code' in json_result):
        return ''
    trans_result = ''
    for i in json.loads(res.content).get('trans_result'):
        trans_result += i.get("dst")+'\n'
    # print(trans_result)
    return trans_result.strip()
