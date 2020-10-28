# -*-coding:utf8-*-
from nonebot import on_command, CommandSession
# from nonebot import scheduler
# from .data_source import saveDatas, loadDatas
# import random
import json
from os import path
# import time
# from datetime import datetime

__plugin_name__ = 'sign'
__plugin_usage__ = r"功能列表:\n签到: .签到"

sign_list = []


@on_command('签到', only_to_me=False)
async def sign(session: CommandSession):
    user_name = session.ctx['sender']['nickname']
    user_id = int(session.ctx['sender']['user_id'])
    if not checkRegister(user_id):
        userdata = {
            'id': user_id,
            'sign_times': 0,
            'sign_today': 0
        }
        sign_list.append(userdata)
        saveDatas()
    for data in sign_list:
        if user_id == data['id']:
            data['sign_times'] += 1
            data['sign_today'] = 1
    text = '[[群内签到]]'
    text += '[CQ:rich,data={"app":"com.tencent.miniapp","desc":"","view":"notification",'
    text += '"ver":"0.0.0.1","prompt":"[群内签到]","meta":{"notification":{"appInfo":{"appName":'
    text += '"群签到"' + ',"appType":4,"appid":1109659848,"iconUrl":' 
    text += '"http:\\/\\/q2.qlogo.cn\\/headimg_dl?dst_uin=2511770171&amp;spec=100"'+'},"data":['
    text += '{"title":"今日签到"'+',"value":"1次"},'
    text += '{"title":"总签到","value":"'+str(data['sign_times'])+'次"},'
    text += '{"title":"总胖次","value":"618胖次"},'
    text += '{"title":"位居本群","value":"第42位"}],'
    text += '"title":"恭喜一天到晚没睡醒前往欧洲的路更进了一步！",'
    text += '"button":[{"name":"本次签到获得33胖次","action":""}],"emphasis_keyword":""}}}]'

    await session.send(text)


def checkRegister(user_id: int) -> bool:
    loadDatas()
    if not sign_list:
        return False
    for data in sign_list:
        if user_id == data['id']:
            return True
    return False


def saveDatas():
    with open("./datas/sign.json", "w") as f:
        json.dump(sign_list, f)
    print(sign_list)


def loadDatas():
    global sign_list
    sign_list.clear()

    if not path.exists("./datas/sign.json"):
        f = open('./datas/sign.json', 'w')
        f.close()
    try:
        with open("./datas/sign.json", 'r') as f:
            sign_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("file empty")
