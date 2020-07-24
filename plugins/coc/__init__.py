# -*-coding:utf8-*-
from nonebot import on_command, CommandSession
from .data_source import rollCard, roll


@on_command('coc', aliases=('车卡'), only_to_me=False)
async def makeCard(session: CommandSession):
    card = await rollCard()
    for msg in card:
        await session.send(msg)


@on_command('roll', aliases=('.r'), only_to_me=False)
async def rollpoint(session: CommandSession):
    reg = session.current_arg_text.strip()
    if not reg:
        await session.send('未输入计算式')
    # base_reg = reg.split("+")
    # reg,sum = roll()

    await session.send('你roll出了10000')


@on_command('check', aliases=('c'), only_to_me=False)
async def check(session: CommandSession):
    reg = session.current_arg_text.strip()
    if not reg:
        await session.send('未输入计算式')
    skill = reg.split(" ")
    await session.send('你的'+skill[0]+'等级为'+skill[1])


@on_command('sancheck', aliases=('sc'), only_to_me=False)
async def sancheck(session: CommandSession):
    await session.send('你失去了100san,疯掉了.')


@on_command('cochelp', aliases=('跑团功能'), only_to_me=False)
async def help(session: CommandSession):
    msg = '功能列表:\n'
    msg += '人物车卡: .coc .车卡\n'
    msg += '指定骰点: .roll .r(格式为.r x1dy1+x2dy2+...+z)\n'
    msg += '技能检定: .sancheck .sc(格式为.sc 意志)\n'
    msg += '理智检定: .check .c(格式为.c 技能名 技能等级)'
    await session.send(msg)
