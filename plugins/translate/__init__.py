# -*-coding:utf8-*-
# from nonebot import scheduler, get_bot
from nonebot import on_command, CommandSession
from .data_source import translate
# from aiocqhttp.exceptions import Error as CQHttpError
# from aiocqhttp import MessageSegment
from time import sleep
# import os


@on_command('tr', only_to_me=False)
async def tr(session: CommandSession):
    reg = session.current_arg_text.strip().split(' ', 2)
    if len(reg) == 3:
        from_reg = reg[0]
        to_reg = reg[1]
        text = reg[2]
        result = translate(text, from_reg, to_reg)
        if result:
            await session.send('翻译:\n' + result)
        else:
            await session.send('格式错误,输入格式:\n.tr 原文语种 目标语种 文本\n.tra 文本(自动检测并翻译为中文)')
    else:
        await session.send('格式错误,输入格式:\n.tr 原文语种 目标语种 文本\n.tra 文本(自动检测并翻译为中文)')


@on_command('tra', only_to_me=False)
async def tra(session: CommandSession):
    reg = session.current_arg_text.strip()
    if reg:
        from_reg = 'auto'
        to_reg = 'zh'
        text = reg
        result = translate(text, from_reg, to_reg)
        await session.send('翻译:\n' + result)
    else:
        await session.send('格式错误,输入格式:\n.tr 原文语种 目标语种 文本\n.tra 文本(自动检测并翻译为中文)')


@on_command('机翻', only_to_me=False)
async def tr_machine(session: CommandSession):
    reg = session.current_arg_text.strip()
    if reg:
        # print('翻译结果:\n英文:%s\n日文:%s' % (en_str, jp_str))
        # await session.send('功能修复中.')
        # bot = get_bot()
        # reg = session.current_arg_text.strip().split(' ')
        # if(reg[0].isdigit()):
        # times = int(reg[0])
        string = reg
        string = translate(string, 'auto', 'zh')
        sleep(1)
        for i in range(0, 2):
            string = translate(string, 'zh', 'wyw')
            # print(string)
            sleep(1)
            string = translate(string, 'wyw', 'jp')
            # print(string)
            sleep(1)
            string = translate(string, 'jp', 'zh')
            # print(string)
            sleep(1)
        await session.send(string)
    else:
        await session.send('格式错误')
