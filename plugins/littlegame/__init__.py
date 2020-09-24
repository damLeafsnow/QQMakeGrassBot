# -*-coding:utf8-*-
from nonebot import on_command, CommandSession
from nonebot import scheduler
# from .data_source import saveDatas, loadDatas
import random
import json
from os import path
import time
from datetime import datetime

__plugin_name__ = 'little game'
__plugin_usage__ = r"功能列表:\n注册: .注册\n种菜: .种菜\n收菜: .收菜\n查询菜价: .查价\n库存: .库存"


# base price
price = 50
gamedata_list = []
plantdata = {'seed': 1800}


@scheduler.scheduled_job('interval', minutes=15)
async def random_price():
    global price
    price = random.randint(15, 120)
    print("新菜价:%d" % price)


@on_command('注册', only_to_me=False)
async def register(session: CommandSession):
    user_name = session.ctx['sender']['nickname']
    user_id = int(session.ctx['sender']['user_id'])
    if checkRegister(user_id):
        await session.send('%s已经注册过了.' % (user_name))
        return
    userdata = {
        'id': user_id,
        'data':
        {
            'username': user_name,
            'gold': 0,
            'plant_state': 0,
            'plant_time': ''
        }
    }
    gamedata_list.append(userdata)
    saveDatas()
    await session.send('%s注册成功.' % (user_name))


@on_command('种菜', only_to_me=False)
async def plant(session: CommandSession):
    user_name = session.ctx['sender']['nickname']
    user_id = int(session.ctx['sender']['user_id'])
    if not checkRegister(user_id):
        await session.send('%s还没有注册,请先注册.' % (user_name))
    for data in gamedata_list:
        if user_id == data['id']:
            if data['data']['plant_state'] == 0:
                data['data']['plant_state'] = 1
                data['data']['plant_time'] = str(datetime.now())
                await session.send('%s于%s开始种菜,剩余%d秒.' % (user_name,
                                                         datetime.now(), plantdata['seed']))
                saveDatas()
            else:
                await session.send('%s的菜已经在种了,剩余%d秒.' % (user_name,
                                                         calLastPlantTime(data['data']['plant_time'])))


@on_command('收菜', only_to_me=False)
async def harvest(session: CommandSession):
    user_name = session.ctx['sender']['nickname']
    user_id = int(session.ctx['sender']['user_id'])
    if not checkRegister(user_id):
        await session.send('%s还没有注册,请先注册.' % (user_name))
    for data in gamedata_list:
        if user_id == data['id']:
            if data['data']['plant_state'] == 0:
                await session.send('%s还没有种菜.' % (user_name))
                return
            else:
                lastTime = calLastPlantTime(data['data']['plant_time'])
                if lastTime == 0:
                    data['data']['plant_state'] = 0
                    data['data']['plant_time'] = ''
                    data['data']['gold'] += price
                    await session.send('%s完成收菜,获得%d元,当前总计%d元' % (user_name,
                                                                 price, data['data']['gold']))
                    saveDatas()
                else:
                    await session.send('%s的菜还有%d秒.' % (user_name, lastTime))


@on_command('查价', only_to_me=False)
async def price(session: CommandSession):
    global price
    await session.send('当前菜价:%d元' % price)


@on_command('库存', only_to_me=False)
async def storage(session: CommandSession):
    user_name = session.ctx['sender']['nickname']
    user_id = int(session.ctx['sender']['user_id'])
    if not checkRegister(user_id):
        await session.send('%s还没有注册,请先注册.' % (user_name))
    for data in gamedata_list:
        if user_id == data['id']:
            await session.send('%s当前拥有%d元' % (user_name, data['data']['gold']))


def calLastPlantTime(plantTime: str) -> int:
    currentTime = datetime.now()
    lastTime = (currentTime-plantTime).seconds
    if lastTime <= 0:
        return 0
    return lastTime


def checkRegister(user_id: int) -> bool:
    loadDatas()
    if not gamedata_list:
        return False
    for data in gamedata_list:
        if user_id == data['id']:
            return True
    return False


def saveDatas():
    with open("./datas/gamedata.json", "w") as f:
        json.dump(gamedata_list, f)
    print(gamedata_list)


def loadDatas():
    global gamedata_list
    gamedata_list.clear()

    if not path.exists("./datas/gamedata.json"):
        f = open('./datas/gamedata.json', 'w')
        f.close()
    try:
        with open("./datas/gamedata.json", 'r') as f:
            gamedata_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("file empty")
