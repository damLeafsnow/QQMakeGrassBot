# -*-coding:utf8-*-
from nonebot import scheduler, get_bot
from nonebot import on_natural_language, NLPSession
from nonebot import on_command, CommandSession
from .data_source import get_bilibili_info_by_avid, get_bilibili_info_by_bvid
from .data_source import get_bilibili_info_by_b23tv, GetDynamicStatus
from .data_source import GetLiveStatus, get_bilibili_live_info, getUserInfobyUID
from aiocqhttp.exceptions import Error as CQHttpError
from time import sleep
import json
from os import path

dynamic_list = {}
live_list = {}
uid_dict = {}
debug_group = 1087849813

__plugin_name__ = 'bilibili'
__plugin_usage__ = r"b站视频直播间解析,动态直播推送\n'1.添加(取消)动态关注+uid 或 biliadddy/bilideldy+uid\n2.添加(取消)直播关注+uid 或 biliaddlive/bilidellive+uid\n3.动态(直播)关注列表 或 bilidylist/bililivelist+uid\n4.用户查询+uid 或 .uid+uid"


# 定时推送列表数据
# @scheduler.scheduled_job('interval',seconds=30) #测试用
@scheduler.scheduled_job('interval', minutes=5)
async def _():
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    bot = get_bot()
    # 获取动态更新
    for key in dynamic_list.keys():
        for uid in dynamic_list[key]:
            sleep(1)
            dynamic_content = GetDynamicStatus(uid, key)
            if dynamic_content:
                await bot.send_group_msg(group_id=debug_group, message=uid+'有新动态,正在推送.')
                for content in dynamic_content:
                    try:
                        await bot.send_group_msg(group_id=key, message=content)
                        sleep(2)
                    except CQHttpError as e:
                        await bot.send_group_msg(group_id=debug_group, message='推送动态信息错误:\n'+str(e))
    # 获取直播更新
    for key in live_list.keys():
        for uid in live_list[key]:
            sleep(1)
            live_msg = GetLiveStatus(uid, key)
            if live_msg:
                await bot.send_group_msg(group_id=debug_group, message=uid+'有新直播消息,正在推送.')
                for content in live_msg:
                    try:
                        await bot.send_group_msg(group_id=key, message=content)
                        sleep(2)
                    except CQHttpError as e:
                        await bot.send_group_msg(group_id=debug_group, message='推送直播信息错误:\n'+str(e))


# 解析收到的av,bv号关键词,通过api读取信息
@on_natural_language({'BV', 'bv', 'av'}, only_to_me=False)
async def biliAlz(session: NLPSession):
    msg = str(session.event["message"])

    # 检索视频号
    list = msg.split('/')
    vid = 0
    info = []
    for i in list:
        if i.startswith('av') or i.startswith('BV') or i.startswith('bv'):
            vid = i
            break

    # 清理可能存在的多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]

    # 获取数据
    if vid.startswith('av'):
        await get_bot().send_group_msg(group_id=debug_group, message='解析到av号:'+vid)
        info = get_bilibili_info_by_avid(vid[2:])
    elif vid.startswith('BV') or i.startswith('bv'):
        await get_bot().send_group_msg(group_id=debug_group, message='解析到BV号:'+vid)
        info = get_bilibili_info_by_bvid(vid)
    if not info:
        await get_bot().send_group_msg(group_id=debug_group, message='解析完成,非b站链接')
        return

    # 消息推送
    for content in info:
        await session.send(content)
        sleep(1)


# 解析加密短链
@on_natural_language({'b23.tv'}, only_to_me=False)
async def bilib23(session: NLPSession):
    msg = str(session.event["message"])

    # 检索视频号
    list = msg.split('/')
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'b23.tv':
            vid = list[i+1]
            break
        i += 1

    # 获取数据
    await get_bot().send_group_msg(group_id=debug_group, message='解析到加密短链:'+vid)
    info = get_bilibili_info_by_b23tv(vid)
    if not info:
        await get_bot().send_group_msg(group_id=debug_group, message='解析完成,非b站链接')
        return

    # 消息推送
    for content in info:
        await session.send(content)
        sleep(1)


#  番剧id解析
# @on_natural_language({'ep'}, only_to_me=False)
# async def biliep(session: NLPSession):
#     msg = str(session.event["message"])
#     list = msg.split('/')
#     # await get_bot().send_group_msg(group_id=debug_group, message='解析结果:\n'+','.join(list))
#     # vid = 0
#     info = []
#     for i in list:
#         if i.startswith('ep'):
#             vid = i
#             break
#     #  清理多余后缀信息
#     if vid.find('?'):
#         vid = vid.split('?')[0]
#     await get_bot().send_group_msg(group_id=debug_group, message='解析到番剧号:'+vid)
#     info = get_bilibili_ep_info(vid)
#     if not info:
#         await get_bot().send_group_msg(group_id=debug_group, message='解析完成,非b站番剧')
#         return
#     for content in info:
#         await session.send(content)
#         sleep(1)
    # await get_bot().send_group_msg(group_id=debug_group, message='解析完成,已推送数据')


#  直播间解析
@on_natural_language({'live'}, only_to_me=False)
async def bililive(session: NLPSession):
    msg = str(session.event["message"])

    # 检索直播间号
    list = msg.split('/')
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'live.bilibili.com':
            vid = list[i+1]
            break
        i += 1

    #  清理多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]

    # 获取数据
    await get_bot().send_group_msg(group_id=debug_group, message='解析到直播间地址:'+vid)
    info = get_bilibili_live_info(vid)
    if not info:
        await get_bot().send_group_msg(group_id=debug_group, message='解析完成,直播间不存在')
        return

    # 消息推送
    for content in info:
        await session.send(content)
        sleep(1)


# 管理关注列表
@on_command('添加动态关注', aliases={'biliadddy'}, only_to_me=False)
async def add_dynamic_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(session.event.group_id)
    uid = session.current_arg_text.strip()
    user_info = getUserInfobyUID(uid)
    msg = ''
    if user_info:
        msg += '已添加到动态关注:\n' + user_info['name']
        msg += '(' + uid + ')\n'
        msg += '[CQ:image,file=' + user_info['face'] + ']'
        msg += '\n性别:' + user_info['sex'] + '\n个人签名:\n' + user_info['sign']

        # 添加uid名称映射
        if uid not in uid_dict.keys():
            uid_dict[uid] = user_info['name']
        saveUIDdata()

        # 添加uid到数据库
        if group in dynamic_list.keys():
            dynamic_list[group].append(uid)
        else:
            dynamic_list[group] = []
            dynamic_list[group].append(uid)
        saveDatas()
    else:
        msg += '未查询到用户.'

    # 消息推送
    await session.send(msg)


@on_command('取消动态关注', aliases={'bilideldy'}, only_to_me=False)
async def del_dynamic_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(session.event.group_id)
    uid = session.current_arg_text.strip()
    msg = ''
    # 删除
    if group in dynamic_list.keys():
        if uid in dynamic_list[group]:
            dynamic_list[group].remove(uid)
            msg += '用户' + str(uid) + '已取消动态关注.'
            saveDatas()
        else:
            msg += '未关注该用户.'
    else:
        msg += '未关注该用户.'

    # 消息推送
    await session.send(msg)


@on_command('添加直播关注', aliases={'biliaddlive'}, only_to_me=False)
async def add_live_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(session.event.group_id)
    uid = session.current_arg_text.strip()
    user_info = getUserInfobyUID(uid)
    msg = ''
    if user_info:
        msg += '已添加到直播关注:\n' + user_info['name']
        msg += '(' + uid + ')\n'
        msg += '[CQ:image,file=' + user_info['face'] + ']'
        msg += '\n性别:' + user_info['sex'] + '\n个人签名:\n' + user_info['sign']

        # 添加uid名称映射
        if uid not in uid_dict.keys():
            uid_dict[uid] = user_info['name']
        saveUIDdata()

        # 添加
        if group in live_list.keys():
            live_list[group].append(uid)
        else:
            live_list[group] = []
            live_list[group].append(uid)
        saveDatas()
    else:
        msg.append += '未查询到用户.'

    await session.send(msg)


@on_command('取消直播关注', aliases={'bilidellive'}, only_to_me=False)
async def del_live_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(session.event.group_id)
    uid = session.current_arg_text.strip()
    msg = ''
    # 删除
    if group in live_list.keys():
        if uid in live_list[group]:
            live_list[group].remove(uid)
            msg += '用户' + str(uid) + '已取消直播关注.'
            saveDatas()
        else:
            msg += '未关注该用户.'
    else:
        msg += '未关注该用户.'
    await session.send(msg)


@on_command('动态关注列表', aliases={'bilidylist'}, only_to_me=False)
async def show_dynamic_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(session.event.group_id)

    msg = ''
    if group in dynamic_list.keys() and dynamic_list[group]:
        msg += '本群(' + group + ')动态关注列表:'
        for uid in dynamic_list[group]:
            if uid in uid_dict.keys():
                msg += '\n' + uid + '(' + uid_dict[uid] + ')'
            else:
                user_info = getUserInfobyUID(uid)
                sleep(1)
                if user_info:
                    # 添加uid名称映射
                    if uid not in uid_dict.keys():
                        uid_dict[uid] = user_info['name']
                    saveUIDdata()
                    msg += '\n' + uid + '(' + uid_dict[uid] + ')'
                else:
                    msg += '\n' + uid + '(用户不存在)'
    else:
        msg += '本群关注列表为空'
    await session.send(msg)


@on_command('直播关注列表', aliases={'bililivelist'}, only_to_me=False)
async def show_live_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
        loadUIDdata()

    group = str(session.event.group_id)

    msg = ''
    if group in live_list.keys() and live_list[group]:
        msg += '本群(' + group + ')直播关注列表:'
        for uid in live_list[group]:
            if uid in uid_dict.keys():
                msg += '\n' + uid + '(' + uid_dict[uid] + ')'
            else:
                user_info = getUserInfobyUID(uid)
                sleep(1)
                if user_info:
                    # 添加uid名称映射
                    if uid not in uid_dict.keys():
                        uid_dict[uid] = user_info['name']
                    saveUIDdata()
                    msg += '\n' + uid + '(' + uid_dict[uid] + ')'
                else:
                    msg += '\n' + uid + '(用户不存在)'
    else:
        msg += '本群关注列表为空'
    await session.send(msg)


@on_command('用户查询', aliases={'uid'}, only_to_me=False)
async def bili_uid_search(session: CommandSession):
    uid = session.current_arg_text.strip()

    # 输入检查
    if not uid or not uid.isdigit():
        await session.send('你uid有问题.')
        return
    
    user_info = getUserInfobyUID(uid)
    msg = ''
    if user_info:
        msg.append('查询到uid'+uid)
        msg.append('[CQ:image,file='+user_info['face']+']')
        msg.append('用户名'+user_info['name']+',性别' +
                   user_info['sex']+',个人签名'+user_info['sign'])

        # 更新uid数据

    else:
        msg.append('未查询到用户.')

    await session.send(msg)


def loadUIDdata():
    global uid_dict
    uid_dict.clear()

    if not path.exists("./datas/uidlist.json"):
        f = open('./datas/uidlist.json', 'w')
        f.close()

    try:
        with open("./datas/uidlist.json", 'r') as f:
            uid_dict = json.load(f)
    except json.decoder.JSONDecodeError:
        print("uidlist file empty")


def saveUIDdata():
    with open("./datas/uidlist.json", "w") as f:
        json.dump(uid_dict, f)


def saveDatas():
    with open("./datas/dynamiclist.json", "w") as f:
        json.dump(dynamic_list, f)
    with open("./datas/livelist.json", "w") as f:
        json.dump(live_list, f)


def loadDatas():
    global dynamic_list, live_list
    dynamic_list.clear()
    live_list.clear()

    if not path.exists("./datas/dynamiclist.json"):
        f = open('./datas/dynamiclist.json', 'w')
        f.close()
    if not path.exists("./datas/livelist.json"):
        f = open('./datas/livelist.json', 'w')
        f.close()

    try:
        with open("./datas/dynamiclist.json", 'r') as f:
            dynamic_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("dynamiclist file empty")
    try:
        with open("./datas/livelist.json", 'r') as f:
            live_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("livelist file empty")
