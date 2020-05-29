# -*-coding:utf8-*-
import nonebot
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand
from aiocqhttp.exceptions import Error as CQHttpError
from datetime import datetime
import random
import requests
import json
import time

name_dict={}
uidlist_list= []
group_list=[]
tempmsg = '' #复读延迟

# bilisearch_switch = False
# repeat_switch = False
# grass_switch = False
#debug
bilisearch_switch = True 
repeat_switch = True
grass_switch = True

nonebot.init()
nonebot.load_builtin_plugins()


def main():
    # 载入数据
    try:
        with open('./data_files/UID_Name_Dict', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line)[:-1].replace(' ', '') #清理/n和空格
                t = str_t.split(',') #分割
                name_dict[t[0]] = t[1]
            f.close()
            # print (name_dict)
    except Exception as err:
        print (err)
        exit()
    try:
        with open('./data_files/UID_List', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line)[:-1].replace(' ', '') #清理/n和空格
                t = str_t.split(',') #分割
                uidlist_list.append(t)
            f.close()
            # print (uidlist_list)
    except Exception as err:
        print (err)
        exit()
    try:
        with open('./data_files/QQ_Group_List', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line)[:-1].replace(' ', '') #清理/n和空格
                group_list.append(str_t)
            f.close()
            # print (group_list)
    except Exception as err:
        print (err)
        exit()

    nonebot.run(host='127.0.0.1', port=8080)

#复读
@on_natural_language(only_to_me=False)
async def repeat(session: NLPSession):
    if repeat_switch:
        global tempmsg
        msg = session.ctx["message"]
        groupnum=str(session.ctx['group_id'])
        print('群%s收到消息%s' % (groupnum, msg))
        if groupnum in group_list:
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

#指令控制
@on_command('启动推送', aliases=('开始推送',), only_to_me=False)
async def start_bilisearch(session: CommandSession):
    global bilisearch_switch
    await hello()
    bilisearch_switch = True

@on_command('关闭推送', aliases=('停止推送','取消推送'), only_to_me=False)
async def close_bilisearch(session: CommandSession):
    global bilisearch_switch
    await session.send('已停止b站动态推送功能')
    bilisearch_switch = False

@on_command('启动复读', aliases=('开始复读',), only_to_me=False)
async def start_repeat(session: CommandSession):
    global repeat_switch
    await session.send('已开启复读功能')
    repeat_switch = True

@on_command('关闭复读', aliases=('停止复读','取消复读'), only_to_me=False)
async def close_repeat(session: CommandSession):
    global repeat_switch
    await session.send('已停止复读功能')
    repeat_switch = False

@on_command('启动生草', aliases=('开始生草',), only_to_me=False)
async def start_grass(session: CommandSession):
    global grass_switch
    await session.send('已开启生草功能')
    grass_switch = True

@on_command('关闭生草', aliases=('停止生草','取消生草'), only_to_me=False)
async def close_grass(session: CommandSession):
    global grass_switch
    await session.send('已停止生草功能')
    grass_switch = False

@on_command('功能列表', aliases=('功能状态'), only_to_me=False)
async def switch_ask(session: CommandSession):
    msg = '当前功能列表:\nb站动态推送  %s\n复读  %s\n生草  %s' % ('启动中' if bilisearch_switch else '已关闭', '启动中' if repeat_switch else '已关闭','启动中' if grass_switch else '已关闭' )
    await session.send(msg)

# @nonebot.scheduler.scheduled_job('interval',seconds=15) #测试用
@nonebot.scheduler.scheduled_job('interval',minutes=5)
async def _():
    # 列表提示
    # global first_start
    # if first_start==True:
    #     await hello()
    #     first_start=False
    if bilisearch_switch:
        bot = nonebot.get_bot()
        for i in range(0, len(group_list)): #遍历所有群
            # for uidlist in uidlist_list: #遍历群索引对应关注列表
            for uid in uidlist_list[i]:         #遍历每个uid
                res=''
                dynamic_content = GetDynamicStatus(uid, i)
                for content in dynamic_content:
                    try:
                        res = await bot.send_group_msg(group_id=group_list[i], message=content)
                    except CQHttpError as e:
                        pass
                #live_status = GetLiveStatus(uidlist_list[i])
                #if live_status != '':
                #    for groupnum in group_list[i]:
                #        await bot.send_group_msg(group_id=groupnum, message=name_list[i] +' 开播啦啦啦！！！ ' + live_status)

async def hello():
    bot = nonebot.get_bot()
    for i in range(0, len(group_list)): #遍历所有群
        hello_msg = '已开启b站动态推送功能,当前关注列表: '
        # for uidlist in uidlist_list: #遍历群索引对应关注列表
        for uid in uidlist_list[i]:         #遍历每个uid
            hello_msg = hello_msg+name_dict[uid]+' '
        # print(hello_msg)
        try:
            hello_msg = await bot.send_group_msg(group_id=group_list[i], message=hello_msg)
        except CQHttpError as e:
            pass

#用户uid 用户名列表索引
def GetDynamicStatus(uid, i):
    res = requests.get('https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid='+str(uid)+'offset_dynamic_id=0')
    res.encoding='utf-8'
    res = res.text
    # print('获取动态数据'+str(res))
    #res = res.encode('utf-8')
    cards_data = json.loads(res)
    cards_data = cards_data['data']['cards']
    try:
        with open('./dynamic_files/'+str(uid)+'_'+str(i)+'Dynamic','r') as f:
            last_dynamic_str = f.read()
            f.close()
    except Exception as err:
        last_dynamic_str=''
        pass
    if last_dynamic_str == '':
        last_dynamic_str = cards_data[1]['desc']['dynamic_id_str']
    print(last_dynamic_str)
    index = 0
    content_list=[]
    cards_data[0]['card'] = json.loads(cards_data[0]['card'],encoding='gb2312')
    nowtime = time.time().__int__()
    # card是字符串，需要重新解析
    while last_dynamic_str != cards_data[index]['desc']['dynamic_id_str']:
        #这条是105 秒前发的。
        if nowtime-cards_data[index]['desc']['timestamp'] > 105:
            break
        try:
            if (cards_data[index]['desc']['type'] == 64):
                content_list.append(name_dict[uid] +'发了新专栏「'+ cards_data[index]['card']['title'] + '」并说： ' +cards_data[index]['card']['dynamic'])
            else:
                if (cards_data[index]['desc']['type'] == 8):
                    content_list.append(name_dict[uid] + '发了新视频「'+ cards_data[index]['card']['title'] + '」并说： ' +cards_data[index]['card']['dynamic'])
                else:         
                    if ('description' in cards_data[index]['card']['item']):
                        #这个是带图新动态
                        content_list.append(name_dict[uid] + '发了新动态： ' +cards_data[index]['card']['item']['description'])
                        print('Fuck')
                        #CQ使用参考：[CQ:image,file=http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg]
                        for pic_info in cards_data[index]['card']['item']['pictures']:
                            content_list.append('[CQ:image,file='+pic_info['img_src']+']')
                    else:
                        #这个表示转发，原动态的信息在 cards-item-origin里面。里面又是一个超级长的字符串……
                        #origin = json.loads(cards_data[index]['card']['item']['origin'],encoding='gb2312') 我也不知道这能不能解析，没试过
                        #origin_name = 'Fuck'
                        if 'origin_user' in cards_data[index]['card']:
                            origin_name = cards_data[index]['card']['origin_user']['info']['uname']
                            content_list.append(name_dict[uid]+ '转发了「'+ origin_name + '」的动态并说： ' +cards_data[index]['card']['item']['content'])
                        else:
                            #这个是不带图的自己发的动态
                            content_list.append(name_dict[uid]+ '发了新动态： ' +cards_data[index]['card']['item']['content'])
            content_list.append('本条动态地址为'+'https://t.bilibili.com/'+ cards_data[index]['desc']['dynamic_id_str'])
        except Exception as err:
                print('PROCESS ERROR')
                pass
        index += 1
#        print(len(cards_data))
#        print(index)
        if len(cards_data) == index:
            break
        cards_data[index]['card'] = json.loads(cards_data[index]['card'])
    f = open('./dynamic_files/'+str(uid)+'_'+str(i)+'Dynamic','w')
    f.write(cards_data[0]['desc']['dynamic_id_str'])
    f.close()
    return content_list


def GetLiveStatus(uid,i):
    res = requests.get('https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid='+str(uid))
    res.encoding = 'utf-8'
    res = res.text
    try:
        with open('./dynamic_files/'+str(uid)+'_'+str(i)+'Live','r') as f:
            last_live_str = f.read()
            f.close()
    except Exception as err:
            last_live_str = '0'
            pass
    live_data = json.loads(res)
    live_data = live_data['data']
    now_live_status = str(live_data['liveStatus'])
    live_title = live_data['title']
    f = open('./dynamic_files/'+str(uid)+'_'+str(i)+'Live','w')
    f.write(now_live_status)
    f.close()
    if last_live_str == '0':
        if now_live_status == '1':
            return live_title
    return ''


if __name__ == "__main__":
    main()

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