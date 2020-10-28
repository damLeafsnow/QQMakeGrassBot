# -*-coding:utf8-*-
# from nonebot import scheduler, get_bot
from nonebot import on_command, CommandSession
from .data_source import translate
# from aiocqhttp.exceptions import Error as CQHttpError
# from aiocqhttp import MessageSegment
from time import sleep
# import os

__plugin_name__ = 'translate'
__plugin_usage__ = r".tr/.翻译 原文语种 目标语种 文本\n.tra/.自动翻译 文本(自动检测并翻译为中文)\n.机翻 文本 获得草生机翻"


@on_command('tr', aliases=('翻译'), only_to_me=False)
async def tr(session: CommandSession):
    reg = session.current_arg_text.strip()  # .split(' ', 2)
    if len(reg) == 3:
        from_reg = reg[0]
        to_reg = reg[1]
        text = reg[2]
        result = translate(text, from_reg, to_reg)
        if result:
            await session.send('翻译:\n' + result)
        else:
            await session.send('格式错误.')
    else:
        await session.send('格式错误.')


@on_command('tra', aliases=('自动翻译'), only_to_me=False)
async def tra(session: CommandSession):
    reg = session.current_arg_text.strip()
    if reg:
        from_reg = 'auto'
        to_reg = 'zh'
        text = reg
        result = translate(text, from_reg, to_reg)
        await session.send('翻译:\n' + result)
    else:
        await session.send('格式错误.')


@on_command('机翻', only_to_me=False)
async def tr_machine(session: CommandSession):
    reg = session.current_arg_text.strip()
    if reg:
        string = reg
        string = translate(string, 'auto', 'zh')
        sleep(1)
        string = translate(string, 'zh', 'wyw')
        print(string)
        sleep(1)
        str_list = list(string)
        str_list.reverse()
        string = ''.join(str_list)
        print(string)
        string = translate(string, 'zh', 'jp')
        print(string)
        sleep(1)
        str_list = list(string)
        str_list.reverse()
        string = ''.join(str_list)
        print(string)
        string = translate(string, 'jp', 'en')
        print(string)
        sleep(1)
        string = translate(string, 'en', 'zh')
        print(string)
        await session.send(string)
    else:
        await session.send('格式错误')
