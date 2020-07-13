# -*-coding:utf8-*-
# import nonebot
from nonebot import init,load_plugins,run
# from nonebot import on_command, CommandSession
# from nonebot import on_natural_language, NLPSession, IntentCommand
# from nonebot import permission as perm
# from aiocqhttp.exceptions import Error as CQHttpError
# from aiocqhttp import MessageSegment
# from datetime import datetime
# import random
# import requests
# import json
# import time
# import os
from os import path
import config

def main():
    # 初始化配置信息
    init(config)
    # 载入插件
    load_plugins(path.join(path.dirname(__file__), 'plugins'), 'plugins')
    # 运行bot
    run()

if __name__ == "__main__":
    main()
            

# #指令控制
# @on_command('启动推送', aliases=('开始推送',), permission=perm.SUPERUSER, only_to_me=False)
# async def start_bilisearch(session: CommandSession):
#     global bilisearch_switch
#     await hello()
#     bilisearch_switch = True

# @on_command('关闭推送', aliases=('停止推送','取消推送'), permission=perm.SUPERUSER, only_to_me=False)
# async def close_bilisearch(session: CommandSession):
#     global bilisearch_switch
#     await session.send('已停止b站动态推送功能')
#     bilisearch_switch = False

# @on_command('启动复读', aliases=('开始复读',), permission=perm.SUPERUSER, only_to_me=False)
# async def start_repeat(session: CommandSession):
#     global repeat_switch
#     await session.send('已开启复读功能')
#     repeat_switch = True

# @on_command('关闭复读', aliases=('停止复读','取消复读'), permission=perm.SUPERUSER, only_to_me=False)
# async def close_repeat(session: CommandSession):
#     global repeat_switch
#     await session.send('已停止复读功能')
#     repeat_switch = False

# @on_command('启动生草', aliases=('开始生草',), permission=perm.SUPERUSER, only_to_me=False)
# async def start_grass(session: CommandSession):
#     global grass_switch
#     await session.send('已开启生草功能')
#     grass_switch = True

# @on_command('关闭生草', aliases=('停止生草','取消生草'), permission=perm.SUPERUSER, only_to_me=False)
# async def close_grass(session: CommandSession):
#     global grass_switch
#     await session.send('已停止生草功能')
#     grass_switch = False

# @on_command('功能列表', aliases=('功能状态'), permission=perm.SUPERUSER, only_to_me=False)
# async def switch_ask(session: CommandSession):
#     msg = '当前功能列表:\nb站动态推送  %s\n复读  %s\n生草  %s' % ('启动中' if bilisearch_switch else '已关闭', '启动中' if repeat_switch else '已关闭','启动中' if grass_switch else '已关闭' )
#     await session.send(msg)



# async def hello():
#     bot = nonebot.get_bot()
#     for i in range(0, len(group_list)): #遍历所有群
#         hello_msg = '已开启b站动态推送功能,当前关注列表: '
#         # for uidlist in uidlist_list: #遍历群索引对应关注列表
#         for uid in uidlist_list[i]:         #遍历每个uid
#             hello_msg = hello_msg+name_dict[uid]+' '
#         # print(hello_msg)
#         try:
#             hello_msg = await bot.send_group_msg(group_id=group_list[i], message=hello_msg)
#         except CQHttpError as e:
#             print(e)






# @on_command('.测试', aliases=('.test'), only_to_me=False)
# async def test(session: CommandSession):
#     await session.send(MessageSegment.image(os.getcwd()+"/grass.jpg"))

# # 关注数据管理
# @on_command('.字典查询', aliases=('.uid'), only_to_me=False)
# async def search_uid_name_dict(session: CommandSession):
#     uid = session.current_arg_text.strip()
#     if not uid:
#         await session.send('你uid呢?')
#         return
#     if uid in name_dict:
#         await session.send('查询到uid'+uid+'->'+name_dict[uid])
#     else:
#         await session.send('uid'+uid+'未添加,可用过\".添加uid uid\"或\".add uid\"添加.')

# @on_command('.添加uid', aliases=('.add'), only_to_me=False)
# async def add_uid_name_dict(session: CommandSession):
#     uid = session.current_arg_text.strip()
#     if not uid:
#         await session.send('你uid呢?')
#         return
#     if uid in name_dict:
#         await session.send('uid'+uid+'('+name_dict[uid]+')'+'已存在.')
#     else:
#         res = requests.get('https://api.bilibili.com/x/space/acc/info?mid='+str(uid))
#         res.encoding = 'utf-8'
#         res = res.text
#         user_data = json.loads(res)
#         data = user_data['data']
#         msg = []
#         msg.append('查询到uid'+uid)
#         msg.append('[CQ:image,file='+data['face']+']')
#         msg.append('用户名'+data['name']+',性别'+data['sex']+',个人签名'+data['sign'])
#         msg.append('已添加到关注字典(不存在的,没写完呢),可通过xxx指令添加到动态关注或直播关注列表(在写了).')
#         for content in msg:
#             try:
#                 res = await session.send(content)
#                 time.sleep(0.2)
#             except CQHttpError as e:
#                 print(e) 




# @on_command('weather', aliases=('的天气', '天气预报', '查天气'))
# async def weather(session: CommandSession):
#     city = session.get('city', prompt='你想查询哪个城市的天气呢？')
#     weather_report = await get_weather_of_city(city)
#     await session.send(weather_report)


# @weather.args_parser
# async def _(session: CommandSession):
#     stripped_arg = session.current_arg_text.strip() 
# 　　 # current_arg_text.strip()是用来去掉字符串的首位空格

#     if session.is_first_run:
#         if stripped_arg:
#             session.state['city'] = stripped_arg
#         return

#     if not stripped_arg:
#         session.pause('要查询的城市名称不能为空呢，请重新输入')

#     session.state[session.current_key] = stripped_arg


# # on_natural_language 装饰器将函数声明为一个自然语言处理器
# # keywords 表示需要响应的关键词，类型为任意可迭代对象，元素类型为 str
# # 如果不传入 keywords，则响应所有没有被当作命令处理的消息
# @on_natural_language(keywords={'的天气'},only_to_me=False)
# async def _(session: NLPSession):
#     # 去掉消息首尾的空白符
#     stripped_msg = session.msg_text.strip()
#     print(stripped_msg)
#     # 对消息进行分词和词性标注
#     words = posseg.lcut(stripped_msg)

#     city = None
#     # 遍历 posseg.lcut 返回的列表
#     for word in words:
#         # 每个元素是一个 pair 对象，包含 word 和 flag 两个属性，分别表示词和词性
#         if word.flag == 'ns':
#             # ns 词性表示地名
#             print(word.flag)
#             city = word.word
#             break

#     # 返回意图命令，前两个参数必填，分别表示置信度和意图命令名
#     return IntentCommand(90.0, 'weather', current_arg=city)