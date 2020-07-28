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
debug_group = 1087849813

__plugin_name__ = 'bilibili'
__plugin_usage__ = r"b站视频直播间解析,动态直播推送"


# 定时推送列表数据


# @scheduler.scheduled_job('interval',seconds=30) #测试用
@scheduler.scheduled_job('interval', minutes=5)
async def _():
    if not dynamic_list or not live_list:
        loadDatas()

    bot = get_bot()
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
                        # print(e)
                        await bot.send_group_msg(group_id=debug_group, message='推送动态信息错误:\n'+str(e))
    for key in live_list.keys():
        for uid in live_list[key]:  # 遍历每个uid
            sleep(1)
            live_msg = GetLiveStatus(uid, key)
            if live_msg:
                await bot.send_group_msg(group_id=debug_group, message=uid+'有新直播消息,正在推送.')
                for content in live_msg:
                    try:
                        await bot.send_group_msg(group_id=key, message=content)
                        sleep(2)
                    except CQHttpError as e:
                        # print(e)
                        await bot.send_group_msg(group_id=debug_group, message='推送直播信息错误:\n'+str(e))
    # await bot.send_group_msg(group_id=debug_group, message='信息推送完成.') #看起来不能一直发

# 收到b站链接


@on_natural_language({'BV', 'bv', 'av'}, only_to_me=False)
async def biliAlz(session: NLPSession):
    # await session.send('你刚才,发了b站链接对吧!', at_sender=True)
    # try:
    #     await get_bot().send_group_msg(group_id=debug_group, message='收到包含BV或av号的信息:\n'+str(session.event["message"]))
    # except CQHttpError as e:
    #     print(e)
    msg = str(session.event["message"])
    list = msg.split('/')
    # await get_bot().send_group_msg(group_id=debug_group, message='解析结果:\n'+','.join(list))
    vid = 0
    info = []
    for i in list:
        if i.startswith('av') or i.startswith('BV'):
            vid = i
            break
    #  清理多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]
    # print(vid)
    if vid.startswith('av'):  # av号(不要av)
        # print(vid)
        await get_bot().send_group_msg(group_id=debug_group, message='解析到av号:'+vid)
        info = get_bilibili_info_by_avid(vid[2:])
    elif vid.startswith('BV'):  # BV号
        await get_bot().send_group_msg(group_id=debug_group, message='解析到BV号:'+vid)
        # print(vid)
        info = get_bilibili_info_by_bvid(vid)
    if not info:
        # await session.send('什么,不是啊,那没事了!', at_sender=True)
        await get_bot().send_group_msg(group_id=debug_group, message='解析完成,非b站链接')
        return
    for content in info:
        await session.send(content)
        sleep(1)
    # await get_bot().send_group_msg(group_id=debug_group, message='解析完成,已推送数据')

# 短链单独分析


@on_natural_language({'b23.tv'}, only_to_me=False)
async def bilib23(session: NLPSession):
    # await session.send('你刚才,发了b站链接对吧!', at_sender=True)
    # try:
    #     await get_bot().send_group_msg(group_id=debug_group, message='收到包含b23的短链信息:\n'+str(session.event["message"]))
    # except CQHttpError as e:
    #     print(e)
    msg = str(session.event["message"])
    list = msg.split('/')
    # await get_bot().send_group_msg(group_id=debug_group, message='解析结果:\n'+','.join(list))
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'b23.tv':
            vid = list[i+1]
            break
        i += 1
    # print(vid)
    await get_bot().send_group_msg(group_id=debug_group, message='解析到加密短链:'+vid)
    info = get_bilibili_info_by_b23tv(vid)
    if not info:
        await get_bot().send_group_msg(group_id=debug_group, message='解析完成,非b站链接')
        # await session.send('什么,不是啊,那没事了!', at_sender=True)
        return
    for content in info:
        await session.send(content)
        sleep(1)
    # await get_bot().send_group_msg(group_id=debug_group, message='解析完成,已推送数据')

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
    list = msg.split('/')
    # await get_bot().send_group_msg(group_id=debug_group, message='解析结果:\n'+','.join(list))
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'live.bilibili.com':
            vid = list[i+1]
            break
        i += 1
    # print(vid)
    #  清理多余后缀信息
    if vid.find('?'):
        vid = vid.split('?')[0]
    await get_bot().send_group_msg(group_id=debug_group, message='解析到直播间地址:'+vid)
    info = get_bilibili_live_info(vid)
    if not info:
        await get_bot().send_group_msg(group_id=debug_group, message='解析完成,直播间不存在')
        # await session.send('什么,不是啊,那没事了!', at_sender=True)
        return
    for content in info:
        await session.send(content)
        sleep(1)
    # await get_bot().send_group_msg(group_id=debug_group, message='解析完成,已推送数据')


# 管理关注列表
@on_command('添加动态关注', aliases={'biliadddy'}, only_to_me=False)
async def add_dynamic_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
    group = str(session.event.group_id)
    uid = session.current_arg_text.strip()
    user_info = getUserInfobyUID(uid)
    msg = []
    if user_info:
        msg.append('查询到uid'+uid)
        msg.append('[CQ:image,file='+user_info['face']+']')
        msg.append('用户名'+user_info['name']+',性别' +
                   user_info['sex']+',个人签名'+user_info['sign'])
        msg.append('已添加到本群动态关注.')

        # 添加
        if group in dynamic_list.keys():
            dynamic_list[group].append(uid)
        else:
            dynamic_list[group] = []
            dynamic_list[group].append(uid)
        saveDatas()
    else:
        msg.append('未查询到用户.')
    for content in msg:
        await session.send(content)


@on_command('取消动态关注', aliases={'bilideldy'}, only_to_me=False)
async def del_dynamic_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
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
    await session.send(msg)


@on_command('添加直播关注', aliases={'biliaddlive'}, only_to_me=False)
async def add_live_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
    group = str(session.event.group_id)
    uid = session.current_arg_text.strip()
    user_info = getUserInfobyUID(uid)
    msg = []
    if user_info:
        msg.append('查询到uid'+uid)
        msg.append('[CQ:image,file='+user_info['face']+']')
        msg.append('用户名'+user_info['name']+',性别' +
                   user_info['sex']+',个人签名'+user_info['sign'])
        msg.append('已添加到本群直播关注.')

        # 添加
        if group in live_list.keys():
            live_list[group].append(uid)
        else:
            live_list[group] = []
            live_list[group].append(uid)
        saveDatas()
    else:
        msg.append('未查询到用户.')
    for content in msg:
        await session.send(content)


@on_command('取消直播关注', aliases={'bilidellive'}, only_to_me=False)
async def del_live_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
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
    await session.send(msg)


@on_command('动态关注列表', aliases={'bilidylist'}, only_to_me=False)
async def add_dynamic_list(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
    group = str(session.event.group_id)
    print(dynamic_list)
    print(group in dynamic_list.keys())
    print(dynamic_list[group])

    msg = ''
    if group in dynamic_list.keys() and dynamic_list[group]:
        msg += '本群(' + group + ')动态关注列表:'
        for uid in dynamic_list[group]:
            msg += '\n' + uid
    else:
        msg += '本群关注列表为空'
    await session.send(msg)


@on_command('直播关注列表', aliases={'bililivelist'}, only_to_me=False)
async def pixiv_analysis(session: CommandSession):
    if not dynamic_list or not live_list:
        loadDatas()
    group = str(session.event.group_id)
    print(live_list)

    msg = ''
    if group in live_list.keys() and live_list[group]:
        msg += '本群(' + group + ')直播关注列表:'
        for uid in live_list[group]:
            msg += '\n' + uid
    else:
        msg += '本群关注列表为空'
    await session.send(msg)


@on_command('用户查询', aliases={'uid'}, only_to_me=False)
async def bili_uid_search(session: CommandSession):
    uid = session.current_arg_text.strip()
    if not uid or not uid.isdigit():
        await session.send('你uid有问题.')
        return
    user_info = getUserInfobyUID(uid)
    msg = []
    if user_info:
        msg.append('查询到uid'+uid)
        msg.append('[CQ:image,file='+user_info['face']+']')
        msg.append('用户名'+user_info['name']+',性别' +
                   user_info['sex']+',个人签名'+user_info['sign'])
    else:
        msg.append('未查询到用户.')
    for content in msg:
        await session.send(content)


@on_command('bili功能列表', aliases={'bilihelp'}, only_to_me=False)
async def bili_help(session: CommandSession):
    msg = '1.添加(取消)动态关注+uid 或 biliadddy/bilideldy+uid\n'
    msg += '2.添加(取消)直播关注+uid 或 biliaddlive/bilidellive+uid\n'
    msg += '3.动态(直播)关注列表 或 bilidylist/bililivelist+uid\n'
    msg += '4.用户查询+uid 或 .uid+uid\n'
    await session.send(msg)


def saveDatas():
    with open("./datas/dynamiclist.json", "w") as f:
        json.dump(dynamic_list, f)
    with open("./datas/livelist.json", "w") as f:
        json.dump(live_list, f)
    print(dynamic_list)
    print(live_list)


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
        print("file empty")
    try:
        with open("./datas/livelist.json", 'r') as f:
            live_list = json.load(f)
    except json.decoder.JSONDecodeError:
        print("file empty")

    # try:
    #     with open('./datas/UID_Live_List', "r", encoding="utf-8") as f:
    #         for line in f:
    #             str_t = str(line).strip()  # 清理/n和空格
    #             t = str_t.split(',')  # 分割
    #             live_list.append(t)
    #         f.close()
    #         # print (live_list)
    # except Exception as err:
    #     print(err)
    #     # await get_bot().send_group_msg(group_id=debug_group, message='读取UID_Live_List文件错误:\n'+str(err))
    #     exit()
    # try:
    #     with open('./datas/UID_List', "r", encoding="utf-8") as f:
    #         for line in f:
    #             str_t = str(line).strip()  # 清理/n和空格
    #             t = str_t.split(',')  # 分割
    #             uidlist_list.append(t)
    #         f.close()
    #         # print (uidlist_list)
    # except Exception as err:
    #     # print (err)
    #     # await get_bot().send_group_msg(group_id=debug_group, message='读取UID_List文件错误:\n'+err)
    #     exit()
    # try:
    #     with open('./datas/QQ_Group_List', "r", encoding="utf-8") as f:
    #         for line in f:
    #             str_t = str(line).strip()  # 清理/n和空格
    #             group_list.append(str_t)
    #         f.close()
    #         # print (group_list)
    # except Exception as err:
    #     print(err)
    #     # await get_bot().send_group_msg(group_id=debug_group, message='读取QQ_Group_List文件错误:\n'+str(err))
    #     exit()
