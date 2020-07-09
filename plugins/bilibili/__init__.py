# -*-coding:utf8-*-
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_bilibili_info_by_avid,get_bilibili_info_by_bvid,get_bilibili_info_by_b23tv
from aiocqhttp.exceptions import Error as CQHttpError
from aiocqhttp import MessageSegment
import time

# 收到b站链接
@on_natural_language({'BV','av'}, only_to_me=False)
async def biliAlz(session: NLPSession):
    # await session.send('你刚才,发了b站链接对吧!', at_sender=True)
    msg = str(session.ctx["message"])
    list = msg.split('/')
    vid = 0
    info = []
    for i in list:
        if i.startswith('av') or i.startswith('BV'):
            vid = i
            break
    # print(vid)
    if vid.startswith('av'):    #av号(不要av)
        # print(vid)
        info = get_bilibili_info_by_avid(vid[2:])
    elif vid.startswith('BV'):  #BV号
        # print(vid)
        info = get_bilibili_info_by_bvid(vid)
    if not info:
        # await session.send('什么,不是啊,那没事了!', at_sender=True)
        return
    for content in info:
        await session.send(content)
        time.sleep(1)

# 短链单独分析
@on_natural_language({'b23.tv/'}, only_to_me=False)
async def bilib23(session: NLPSession):
    # await session.send('你刚才,发了b站链接对吧!', at_sender=True)
    msg = str(session.ctx["message"])
    list = msg.split('/')
    info = []
    vid = ''
    i = 0
    for s in list:
        if s == 'b23.tv':
            vid = list[i+1]
            break
        i+=1
    print(vid)
    info = get_bilibili_info_by_b23tv(vid)
    if not info:
        # await session.send('什么,不是啊,那没事了!', at_sender=True)
        return
    for content in info:
        await session.send(content)
        time.sleep(1)