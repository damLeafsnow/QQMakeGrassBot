# -*-coding:utf8-*-
from nonebot import scheduler, get_bot
from nonebot import on_command, CommandSession
from .data_source import searchByTag, getPic
from aiocqhttp.exceptions import Error as CQHttpError
from aiocqhttp import MessageSegment
from time import sleep
import os

__plugin_name__ = 'pixiv'
__plugin_usage__ = r".pixivnum .pixivpage .pixivmark设置搜索,.pixiv 关键字 搜索"


debug_group = 1087849813
num = 5
page = 5
bookmark = 1000


@on_command('pixiv', only_to_me=False)
async def pixiv_analysis(session: CommandSession):
    # await session.send('功能修复中.')
    bot = get_bot()
    reg = session.current_arg_text
    # seq = MessageSegment.image(os.getcwd()+'\\pixdata\\0.jpg')
    # await bot.send_group_msg(group_id=debug_group, message=seq)

    # try:
    # await bot.send_group_msg(group_id=debug_group,
    #  message='[CQ:image,file=https://img.cheerfun.dev:233/c/540x540_70/img-master/img/2019/12/26/10/47/03/78484613_p0_master1200.jpg]')
    #  message='[CQ:image,file=https://img.cheerfun.dev:233/c/540x540_70/img-master/img/2019/12/26/10/47/03/78484613_p0_master1200.jpg]')
    # except CQHttpError as e:
    # print(e)

    if not reg:
        await session.send('未输入搜索关键词.')
    await bot.send_group_msg(group_id=debug_group, message='p站搜索中,tag:'+reg)
    await session.send("当前参数: 查找%d张图片,搜索页数%d,最低收藏数%d,正在搜索..." % (num, page, bookmark))
    datas = searchByTag(reg, num, page, bookmark)
    # print(ill)
    if not datas:
        await session.send('未搜索到图片或网络错误.')
    else:
        await session.send('搜索到%d组图片.' % len(datas))
    for data in datas:
        await session.send(data[0])
        for i in range(1, len(data)):
            seq = MessageSegment.image(os.getcwd()+'\\pixdata\\'+data[i])
            try:
                await session.send(seq)
            except CQHttpError as e:
                print(e)
            sleep(2)


@on_command('acg', only_to_me=False)
async def setu(session: CommandSession):
    if getPic():
        seq = MessageSegment.image(os.getcwd()+'\\pixdata\\x.png')
        await session.send(seq)


@on_command('pixivpage', only_to_me=False)
async def pixiv_pageset(session: CommandSession):
    global page
    reg = session.current_arg_text.strip()
    if reg.isdigit():
        if int(reg) <= 0:
            await session.send('爬.', at_sender=True)
            return
        page = int(reg)
        await session.send('搜索页数已修改为%d页.' % page)
    else:
        await session.send('数字格式错误.')


@on_command('pixivmark', only_to_me=False)
async def pixiv_markset(session: CommandSession):
    global bookmark
    reg = session.current_arg_text.strip()
    if reg.isdigit():
        if int(reg) <= 0:
            await session.send('爬.', at_sender=True)
            return
        bookmark = int(reg)
        await session.send('最低收藏数已修改为%d.' % bookmark)
    else:
        await session.send('数字格式错误.')


@on_command('pixivnum', only_to_me=False)
async def pixiv_numset(session: CommandSession):
    global num
    reg = session.current_arg_text.strip()
    if reg.isdigit():
        if int(reg) <= 0:
            await session.send('爬.', at_sender=True)
            return
        num = int(reg)
        await session.send('查找图片数已修改为%d.' % num)
    else:
        await session.send('数字格式错误.')

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
