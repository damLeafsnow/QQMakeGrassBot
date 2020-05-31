# -*-coding:utf8-*-
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot import on_command, CommandSession
from nonebot import permission as perm
# import sys
# sys.path.append('..')
# import globalvar as gl

#不对劲
@on_natural_language({'对劲', '问题', '草'}, only_to_me=False)
async def question(session: NLPSession):
    if grass_switch:
        msg = session.ctx["message"]
        groupnum=str(session.ctx['group_id'])
        if groupnum in group_list:
            rnd = random.randint(1, 100)
            print('问题随机数:%d' % (rnd))
            if rnd <= 5:
                await session.send('不对劲')
            if rnd >= 95:
                await session.send('你有问题', at_sender=True)
            if rnd in range(45, 55):
                await session.send('啊,这')


@on_command('启动生草', aliases=('开始生草',), permission=perm.SUPERUSER, only_to_me=False)
async def start_grass(session: CommandSession):
    global grass_switch
    await session.send('已开启生草功能')
    grass_switch = True

@on_command('关闭生草', aliases=('停止生草','取消生草'), permission=perm.SUPERUSER, only_to_me=False)
async def close_grass(session: CommandSession):
    global grass_switch
    await session.send('已停止生草功能')
    grass_switch = False