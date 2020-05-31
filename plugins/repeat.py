# -*-coding:utf8-*-
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import on_command, CommandSession
from nonebot import permission as perm
import random
# import sys
# sys.path.append('..')
# import globalvar as gl

# repeat_switch = False
tempmsg = ''
gl.set_value('repeat_switch', False)

#复读
@on_natural_language(only_to_me=False)
async def repeat(session: NLPSession):
    # if gl.get_value('repeat_switch'):
    global tempmsg
    msg = session.ctx["message"]
    groupnum=str(session.ctx['group_id'])
    print('群%s收到消息%s' % (groupnum, msg))
    if groupnum in gl.get_value('group_list'):
        rnd = random.randint(1, 100)
        print('复读随机数:%d' % (rnd))
        if rnd <= 3:
            print('生草')
            await session.send('草', at_sender=True)
        if rnd >= 97:
            print('复读')
            await session.send(msg)
        if rnd in range(26, 36):
            print('记录延迟复读')
            tempmsg = msg
        if rnd in range(20, 25):
            print('复读延迟复读')
            await session.send(tempmsg)
            tempmsg = '还行'

@on_command('启动复读', aliases=('开始复读',), permission=perm.SUPERUSER, only_to_me=False)
async def start_repeat(session: CommandSession):
    await session.send('已开启复读插件')
    gl.set_value('repeat_switch', True)

@on_command('关闭复读', aliases=('停止复读','取消复读'), permission=perm.SUPERUSER, only_to_me=False)
async def close_repeat(session: CommandSession):
    await session.send('已停止复读插件')
    gl.set_value('repeat_switch', False)