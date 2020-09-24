# -*-coding:utf8-*-
from nonebot import on_natural_language, NLPSession, IntentCommand
from aiocqhttp import MessageSegment
from random import randint
# from .data_source import rollCard,roll

__plugin_name__ = 'makegrass'
__plugin_usage__ = r"复读,生草回复等"


tempmsg = []  # 复读延迟

# 复读


@on_natural_language(only_to_me=False)
async def repeat(session: NLPSession):
    global tempmsg
    msg = session.event["message"]
    groupnum = str(session.event['group_id'])
    print('群%s收到消息%s' % (groupnum, msg))
    # if groupnum in group_list:
    rnd = randint(1, 100)
    # 总概率
    if rnd <= 5:
        rnd = randint(1, 6)
        print('复读随机数:%d' % (rnd))
        if rnd == 1:
            print('生草')
            await session.send('草', at_sender=True)
        if rnd == 2:
            print('复读')
            if session.msg_images:
                seq = MessageSegment.image(session.msg_images[0])
                await session.send(seq)
            else:
                await session.send(msg)
        if rnd in range(3, 5):
            print('记录延迟复读')
            tempmsg.append(msg)
        if rnd in range(5, 7):
            print('复读延迟复读')
            if tempmsg:  # 判断非空
                i = randint(0, len(tempmsg)-1)
                await session.send(tempmsg[i])
                tempmsg.remove(tempmsg[i])
        if rnd == 66:
            await session.send('详情点击:http://game.granbluefantasy.jp/')


# 反问
@on_natural_language({'你', '我', '不', '没', '吗', '?', '？'}, only_to_me=False)
async def ask(session: NLPSession):
    rnd = randint(1, 100)
    if rnd <= 5:
        msg = str(session.event["message"]).strip('?？吗')+'!'
        if (len(msg) >= 3):
            msg = msg.replace('不过', '')
            msg = msg.replace('不', '')
            msg = msg.replace('没', '')
            msg = msg.replace('你', '乪')
            msg = msg.replace('我', '你')
            msg = msg.replace('乪', '我')
            await session.send(msg, at_sender=True)


# 生草
@on_natural_language({'对劲', '问题', '草', '行', '啊', '有一说一', '确实', '没错', '可以', '好',
                      '坏', '成精', '来了', '走了'}, only_to_me=False)
async def grass(session: NLPSession):
    # if grass_switch:
    # msg = session.ctx["message"]
    # groupnum=str(session.ctx['group_id'])
    # if groupnum in group_list:
    rnd = randint(1, 100)
    print('问题随机数:%d' % (rnd))
    # 总概率
    if rnd <= 10:
        rnd = randint(1, 16)
        if rnd <= 1:
            await session.send('不对劲')
        if rnd == 2:
            await session.send('你有问题', at_sender=True)
        if rnd == 5:
            await session.send(u'؟?ذذ؟??¿؟زز¿؟¿???ذ¿')
        if rnd == 6:
            await session.send('我觉得不行')
        if rnd == 7:
            await session.send('你很懂哦')
        if rnd == 9:
            await session.send('挺好')
        if rnd == 10:
            await session.send('确实', at_sender=True)
        if rnd == 11:
            await session.send('好', at_sender=True)
        if rnd == 12:
            await session.send('我觉得ok')
        if rnd == 13:
            await session.send('你这不行')
        if rnd == 14:
            await session.send('溜了溜了')
        if rnd == 15:
            await session.send('这不好吧')
        if rnd == 16:
            await session.send('?')
# yygq


@on_natural_language({'就这', '应该', '懂', '在', '知道', '会', '看'},
                     only_to_me=False)
async def human(session: NLPSession):
    rnd = randint(1, 100)
    print('问题随机数:%d' % (rnd))
        # 总概率
    if rnd <= 10:
        rnd = randint(1, 22)
        if rnd <= 5:
            await session.send('不会吧?不会吧?不会有人看这个吧?')
        if rnd in range(6, 9):
            await session.send('啊,这')
        if rnd in range(11, 13):
            await session.send('就这?', at_sender=True)
        if rnd in range(16, 19):
            await session.send('有事?', at_sender=True)
        if rnd in range(21, 23):
            await session.send('你在教我做事?', at_sender=True)


# 后浪
@on_natural_language({'后浪'}, only_to_me=False)
async def hl(session: NLPSession):
    rnd = randint(1, 100)
    print('后浪浓度:%d' % (rnd))
    if rnd <= 10:
        await session.send('不愧是后浪.')
