# -*-coding:utf8-*-
from nonebot import on_natural_language, NLPSession, IntentCommand
from .data_source import get_bilibili_info
from aiocqhttp.exceptions import Error as CQHttpError
from aiocqhttp import MessageSegment

# 收到b站链接
#https://b23.tv/js0v5D
#https://www.bilibili.com/video/BV1yt4y1Q7DG
#,'b23.tv/'
@on_natural_language({'bilibili.com/video/BV'}, only_to_me=False)
async def biliAlz(session: NLPSession):
    await session.send('你刚才,发了b站链接对吧!', at_sender=True)
    msg = str(session.ctx["message"])
    bvid = msg.split('/')[-1]
    info = get_bilibili_info(bvid)
    for content in info:
        await session.send(content)
    # for i in (0,len(info)):
    #     try:
    #         res = await session.send(info[i])
    #     except CQHttpError as e:
    #         print(e) 

