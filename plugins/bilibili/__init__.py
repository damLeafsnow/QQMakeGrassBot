# -*-coding:utf8-*-
from nonebot import scheduler, get_bot
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_bilibili_info_by_avid, get_bilibili_info_by_bvid, get_bilibili_info_by_b23tv, GetDynamicStatus, GetLiveStatus
from aiocqhttp.exceptions import Error as CQHttpError
from time import sleep

name_dict = {}
uidlist_list = []
group_list = []
live_list = []
debug_group = 1087849813

# 定时推送列表数据
# @scheduler.scheduled_job('interval',seconds=30) #测试用


@scheduler.scheduled_job('interval', minutes=5)
async def _():
    loadDatas()
    # if bilisearch_switch:
    bot = get_bot()
    for i in range(0, len(group_list)):  # 遍历所有群
        # for uidlist in uidlist_list: #遍历群索引对应关注列表
        if i < len(uidlist_list):
            for uid in uidlist_list[i]:  # 遍历每个uid
                sleep(1)
                dynamic_content = GetDynamicStatus(uid, name_dict[uid], i)
                if dynamic_content:
                    await bot.send_group_msg(group_id=debug_group, message=name_dict[uid]+'有新动态,正在推送.')
                    for content in dynamic_content:
                        try:
                            await bot.send_group_msg(group_id=group_list[i], message=content)
                            sleep(0.2)
                        except CQHttpError as e:
                            # print(e)
                            await bot.send_group_msg(group_id=debug_group, message='推送动态信息错误:\n'+str(e))
        if i < len(live_list):
            for uid in live_list[i]:  # 遍历每个uid
                sleep(1)
                live_msg = GetLiveStatus(uid, name_dict[uid], i)
                if live_msg:
                    await bot.send_group_msg(group_id=debug_group, message=name_dict[uid]+'有新直播消息,正在推送.')
                    for content in live_msg:
                        try:
                            await bot.send_group_msg(group_id=group_list[i], message=content)
                            sleep(0.2)
                        except CQHttpError as e:
                            # print(e)
                            await bot.send_group_msg(group_id=debug_group, message='推送直播信息错误:\n'+str(e))
    # await bot.send_group_msg(group_id=debug_group, message='信息推送完成.') #看起来不能一直发

# 收到b站链接


@on_natural_language({'BV', 'av'}, only_to_me=False)
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


@on_natural_language({'b23'}, only_to_me=False)
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


def loadDatas():
    name_dict.clear()
    live_list.clear()
    uidlist_list.clear()
    group_list.clear()
    try:
        with open('./datas/UID_Name_Dict', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line).strip()  # 清理/n和空格
                t = str_t.split(',')  # 分割
                name_dict[t[0]] = t[1]
            f.close()
            # print (name_dict)
    except Exception as err:
        print(err)
        # await get_bot().send_group_msg(group_id=debug_group, message='读取UID_Name_Dict文件错误:\n'+str(err))
        exit()
    try:
        with open('./datas/UID_Live_List', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line).strip()  # 清理/n和空格
                t = str_t.split(',')  # 分割
                live_list.append(t)
            f.close()
            # print (live_list)
    except Exception as err:
        print(err)
        # await get_bot().send_group_msg(group_id=debug_group, message='读取UID_Live_List文件错误:\n'+str(err))
        exit()
    try:
        with open('./datas/UID_List', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line).strip()  # 清理/n和空格
                t = str_t.split(',')  # 分割
                uidlist_list.append(t)
            f.close()
            # print (uidlist_list)
    except Exception as err:
        # print (err)
        # await get_bot().send_group_msg(group_id=debug_group, message='读取UID_List文件错误:\n'+err)
        exit()
    try:
        with open('./datas/QQ_Group_List', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line).strip()  # 清理/n和空格
                group_list.append(str_t)
            f.close()
            # print (group_list)
    except Exception as err:
        print(err)
        # await get_bot().send_group_msg(group_id=debug_group, message='读取QQ_Group_List文件错误:\n'+str(err))
        exit()
