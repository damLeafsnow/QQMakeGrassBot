# -*-coding:utf8-*-
from nonebot import on_command, CommandSession
from nonebot import permission as perm
import urllib.request
from urllib.request import urlopen
import requests
import sys
import ssl
import importlib
import json
importlib.reload(sys)
# import globalvar as gl

gl.set_value('weather_switch', False)

# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气查询」「查天气」
@on_command('weather', aliases=('天气', '查天气', '天气查询'), only_to_me=False)
async def weather(session: CommandSession):
    if gl.get_value('weather_switch'):
        city = session.get('city', prompt='你说哪个城市?')    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
        weather_report = await get_weather_of_city(city)
        await session.send(weather_report)

# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def _(session: CommandSession):
    if gl.get_value('weather_switch'):
        # 清理首尾空白符号
        stripped_arg = session.current_arg_text.strip()
        if session.is_first_run:    # 该命令第一次运行（第一次进入命令会话）
            if stripped_arg:        # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入,例如用户可能发送了：天气 南京
                session.state['city'] = stripped_arg
            return
        
        if not stripped_arg:
            # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
            # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
            session.pause('不能查询无名城市,重新输入.')

        # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
        session.state[session.current_key] = stripped_arg

async def get_weather_of_city(city: str) -> str:
    host = 'http://wthrcdn.etouch.cn/weather_mini?city='
    url = host + urllib.parse.quote(city)
    r = requests.get(url)
    jsons = json.loads(r.text)
    str = city+'的天气为：\n'
    len = 0
    for i in jsons['data']['forecast']:
        if len < 2:
            if len == 0:
                str += '今日：'
            if len == 1:
                str += '明日：'
            str += i['date']
            str += '\n天气：'
            str += i['type']
            str += '\n最'
            str += i['low']
            str += '\n最'
            str += i['high']
            str += '\n'
            len += 1
    return str

@on_command('启动天气', aliases=('开始天气',), permission=perm.SUPERUSER, only_to_me=False)
async def start_weather(session: CommandSession):
    await session.send('已开启天气插件')
    gl.set_value('weather_switch', True)

@on_command('关闭天气', aliases=('停止天气','取消天气'), permission=perm.SUPERUSER, only_to_me=False)
async def close_weather(session: CommandSession):
    await session.send('已关闭天气插件')
    gl.set_value('weather_switch', False)