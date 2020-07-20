# -*-coding:utf8-*-
from nonebot import scheduler, get_bot
from nonebot import on_command, CommandSession
from .data_source import searchByTag, getPic
from aiocqhttp.exceptions import Error as CQHttpError
from aiocqhttp import MessageSegment
from time import sleep
import os

debug_group = 1087849813


@on_command('pixiv', only_to_me=False)
async def pixiv_analysis(session: CommandSession):
    bot = get_bot()
    reg = session.current_arg_text.strip()
    await bot.send_group_msg(group_id=debug_group, message='p站搜索中,tag:'+reg)
    if not reg:
        await session.send('未输入搜索关键词.')
    ill = searchByTag(reg)
    # print(ill)
    if not ill:
        await session.send('未搜索到图片.')
    # await session.send('搜索到前五张图片:')
    await session.send(ill[0])
    for i in range(1, len(ill)):
        # await session.send(content)
        seq = MessageSegment.image(os.getcwd()+ill[i])
        await session.send(seq)
        sleep(1)


@on_command('acg', only_to_me=False)
async def setu(session: CommandSession):
    if getPic():
        seq = MessageSegment.image(os.getcwd()+'\\pixdata\\x.png')
        await session.send(seq)

# 定时推送排行榜
# @scheduler.scheduled_job('interval', minutes=5)
# async def _():
    # loadDatas()
    # # if bilisearch_switch:
    # bot = get_bot()
    # for i in range(0, len(group_list)):  # 遍历所有群
    #     # for uidlist in uidlist_list: #遍历群索引对应关注列表
    #     if i < len(uidlist_list):
    #         for uid in uidlist_list[i]:  # 遍历每个uid
    #             sleep(1)
    #             dynamic_content = GetDynamicStatus(uid, name_dict[uid], i)
    #             if dynamic_content:
    #                 await bot.send_group_msg(group_id=debug_group, message=name_dict[uid]+'有新动态,正在推送.')
    #                 for content in dynamic_content:
    #                     try:
    #                         await bot.send_group_msg(group_id=group_list[i], message=content)
    #                         sleep(0.2)
    #                     except CQHttpError as e:
    #                         # print(e)
    #                         await bot.send_group_msg(group_id=debug_group, message='推送动态信息错误:\n'+str(e))
    #     if i < len(live_list):
    #         for uid in live_list[i]:  # 遍历每个uid
    #             sleep(1)
    #             live_msg = GetLiveStatus(uid, name_dict[uid], i)
    #             if live_msg:
    #                 await bot.send_group_msg(group_id=debug_group, message=name_dict[uid]+'有新直播消息,正在推送.')
    #                 for content in live_msg:
    #                     try:
    #                         await bot.send_group_msg(group_id=group_list[i], message=content)
    #                         sleep(0.2)
    #                     except CQHttpError as e:
    #                         # print(e)
    #                         await bot.send_group_msg(group_id=debug_group, message='推送直播信息错误:\n'+str(e))
    # # await bot.send_group_msg(group_id=debug_group, message='信息推送完成.') #看起来不能一直发
