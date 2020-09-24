# from urllib.request import urlopen
import requests
import json
import time
from os import path, mkdir
from bs4 import BeautifulSoup
import re
from time import sleep


def get_bilibili_info_by_avid(avid: str) -> []:
    res = requests.get(
        'https://api.bilibili.com/x/web-interface/view?aid='+str(avid))
    res.encoding = 'utf-8'
    res = res.text
    info = json.loads(res)
    if info['code'] != 0:  # 解析错误
        return []

    data = info['data']
    owner = data['owner']
    info = []
    info.append('标题:'+data['title']+'UP主:'+owner['name'] +
                '\n简介:'+data['desc']+'\n分类:'+data['tname']+'\n')
    info.append('[CQ:image,file='+data['pic']+']')
    info.append('视频链接:\nhttps://www.bilibili.com/video/' +
                data['bvid']+'\n\nhttps://www.bilibili.com/video/av'+str(data['aid']))
    return info


def get_bilibili_info_by_bvid(bvid: str) -> []:
    res = requests.get(
        'http://api.bilibili.com/x/web-interface/view?bvid='+str(bvid))
    res.encoding = 'utf-8'
    res = res.text
    info = json.loads(res)
    if info['code'] != 0:  # 解析错误
        return []

    data = info['data']
    owner = data['owner']
    info = []
    info.append('标题:'+data['title']+'UP主:'+owner['name'] +
                '\n简介:'+data['desc']+'\n分类:'+data['tname']+'\n')
    info.append('[CQ:image,file='+data['pic']+']')
    info.append('视频链接:\nhttps://www.bilibili.com/video/' +
                data['bvid']+'\n\nhttps://www.bilibili.com/video/av'+str(data['aid']))
    return info


def get_bilibili_info_by_b23tv(b23str: str) -> []:
    res = requests.get('https://b23.tv/'+b23str)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    for tag in soup.find_all(re.compile("^meta")):
        if tag['content'].startswith('https://www.bilibili.com/video/av'):
            vid = tag['content'].split('/')[-2][2:]
            return get_bilibili_info_by_avid(vid)


# def get_bilibili_ep_info(epid: str) -> []:
#     res = requests.get(
#         'https://api.bilibili.com/x/web-interface/view?aid='+str(epid))
#     res.encoding = 'utf-8'
#     res = res.text
#     info = json.loads(res)
#     if info['code'] != 0:  # 解析错误
#         return []

#     data = info['data']
#     owner = data['owner']
#     info = []
#     info.append('标题:'+data['title']+'UP主:'+owner['name'] +
#                 '\n简介:'+data['desc']+'\n分类:'+data['tname']+'\n')
#     info.append('[CQ:image,file='+data['pic']+']')
#     info.append('视频链接:\nhttps://www.bilibili.com/video/' +
#                 data['bvid']+'\n\nhttps://www.bilibili.com/video/av'+str(data['aid']))
#     return info


def get_bilibili_live_info(uid: str) -> []:
    uid = getUIDbyLiveid(uid)
    user_info = getUserInfobyUID(uid)
    live_info = getLiveStatusbyUID(uid)
    # print(user_info)
    # print(live_info)
    # 用户不存在
    # 用户没有直播间
    if not uid or not user_info or not live_info:
        return []

    user_name = user_info['name']
    user_face = user_info['face']
    live_state = live_info['liveStatus']
    live_title = live_info['title']
    live_url = live_info['url']
    live_cover = live_info['cover']
    live_watcher = str(live_info['online'])

    msg = []
    msg.append('这是'+user_name+'的直播间.')
    msg.append('[CQ:image,file='+user_face+']')
    if live_state == 1:
        msg.append('正在直播,直播标题:' + live_title)
        msg.append('[CQ:image,file='+live_cover+']')
        msg.append('直播地址:'+live_url+'\n当前观看人数:'+live_watcher)
    else:
        msg.append('当前未开播.')
    return msg


def GetDynamicStatus(uid, i):
    res = requests.get(
        'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid='+str(uid)+'offset_dynamic_id=0')
    res.encoding = 'utf-8'
    res = res.text
    cards_data = json.loads(res)
    cards_data = cards_data['data']['cards']
    user_info = getUserInfobyUID(uid)

    if not path.exists('./dynamics/'):
        mkdir('./dynamics')
    try:
        with open('./dynamics/'+str(uid)+'_'+str(i)+'Dynamic', 'r') as f:
            last_dynamic_str = f.read()
            f.close()
    except Exception as err:
        last_dynamic_str = ''
        print(err)
    if last_dynamic_str == '':
        last_dynamic_str = cards_data[1]['desc']['dynamic_id_str']
    # print(last_dynamic_str)

    index = 0
    content_list = []
    cards_data[0]['card'] = json.loads(
        cards_data[0]['card'], encoding='gb2312')
    nowtime = time.time().__int__()
    # card是字符串，需要重新解析
    while last_dynamic_str != cards_data[index]['desc']['dynamic_id_str']:
        # 这条是600秒前发的。
        if nowtime-cards_data[index]['desc']['timestamp'] > 600:
            break
        try:
            if (cards_data[index]['desc']['type'] == 64):
                content_list.append(
                    user_info['name'] + '发了新专栏「' + cards_data[index]['card']['title'] + '」并说： ' + cards_data[index]['card']['dynamic'])
                imageurls = cards_data[index]['card']['image_urls']
                if imageurls:
                    for images in cards_data[index]['card']['image_urls']:
                        content_list.append('[CQ:image,file='+images+']')
            else:
                if (cards_data[index]['desc']['type'] == 8):
                    content_list.append(
                        user_info['name'] + '发了新视频「' + cards_data[index]['card']['title'] + '」并说： ' + cards_data[index]['card']['dynamic'])
                    content_list.append(
                        '[CQ:image,file='+cards_data[index]['card']['pic']+']')
                else:
                    if ('description' in cards_data[index]['card']['item']):
                        # 带图新动态
                        content_list.append(
                            user_info['name'] + '发了新动态： ' + cards_data[index]['card']['item']['description'])
                        # CQ使用参考：[CQ:image,file=http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg]
                        for pic_info in cards_data[index]['card']['item']['pictures']:
                            content_list.append(
                                '[CQ:image,file='+pic_info['img_src']+']')
                    else:
                        # 转发动态
                        if 'origin_user' in cards_data[index]['card']:
                            origin_name = cards_data[index]['card']['origin_user']['info']['uname']
                            content_list.append(
                                user_info['name'] + '转发了「' + origin_name + '」的动态并说： ' + cards_data[index]['card']['item']['content'])
                        else:
                            # 这个是不带图的自己发的动态
                            content_list.append(
                                user_info['name'] + '发了新动态： ' + cards_data[index]['card']['item']['content'])
            content_list.append('本条动态地址为'+'https://t.bilibili.com/' +
                                cards_data[index]['desc']['dynamic_id_str'])
        except Exception as err:
            print('PROCESS ERROR')
            print(err)
        index += 1
#        print(len(cards_data))
#        print(index)
        if len(cards_data) == index:
            break
        cards_data[index]['card'] = json.loads(cards_data[index]['card'])
    f = open('./dynamics/'+str(uid)+'_'+str(i)+'Dynamic', 'w')
    f.write(cards_data[0]['desc']['dynamic_id_str'])
    f.close()
    return content_list


def GetLiveStatus(uid, i):
    try:
        with open('./dynamics/'+str(uid)+'_'+str(i)+'Live', 'r') as f:
            last_live_str = f.read()
            f.close()
    except Exception as err:
        last_live_str = '0'
        print(err)
    live_data = getLiveStatusbyUID(str(uid))
    user_info = getUserInfobyUID(uid)
    if live_data and user_info:
        now_live_status = str(live_data['liveStatus'])
        f = open('./dynamics/'+str(uid)+'_'+str(i)+'Live', 'w')
        f.write(now_live_status)
        f.close()
        if last_live_str == '0':
            if now_live_status == '1':
                live_title = live_data['title']
                live_url = live_data['url']
                live_cover = live_data['cover']
                live_watcher = str(live_data['online'])
                live_msg = []
                live_msg.append(user_info['name'] + '直播中:' + live_title)
                live_msg.append('[CQ:image,file='+live_cover+']')
                live_msg.append('直播地址:'+live_url+'\n当前观看人数:'+live_watcher)
                return live_msg
    return ''


# 将直播间id转换为up主uid
def getUIDbyLiveid(liveid: str) -> str:
    header = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }
    res = requests.get('https://live.bilibili.com/'+liveid, headers=header)
    res.encoding = 'utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')

    json_text = ''
    for tag in soup.find_all(re.compile("^script")):
        if str(tag).startswith('<script>window'):
            json_text = str(tag).split('=', 1)[1][:-9]
            break
    js = json.loads(json_text)
    print(js['roomInitRes']['data']['uid'])
    return str(js['roomInitRes']['data']['uid'])


# 根据uid查询直播状态
def getLiveStatusbyUID(uid: str) -> {}:
    header = {
        'authority': 'api.live.bilibili.com',
        'method': 'GET',
        'path': '/room/v1/Room/getRoomInfoOld?mid='+uid,
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'cache-control': 'max-age=0',
        'cookie': '_uuid=A92C9771-F0BF-7E52-1664-CCFF8D51A54653220infoc; buvid3=3725FDC3-E875-4E7F-9B0A-753B3D947C5553949infoc; LIVE_BUVID=AUTO1315839956368027; rpdid=|(kk|JRYk|0J\'ul)JmmlYJ~; DedeUserID=1855051; DedeUserID__ckMd5=e3ecf791def0522f; INTVER=-1; CURRENT_QUALITY=80; Hm_lvt_8a6e55dbd2870f0f5bc9194cddf32a02=1585215103,1585797622; sid=5uu34586; SESSDATA=0a4c1c88%2C1609644074%2Ce51af*71; bili_jct=f993a0f13daff3ca01a871ce32f14ac3; CURRENT_FNVAL=80; blackside_state=1; _dfcaptcha=0584e3b18ca8e0141f6e386a65b7a67c; PVID=14',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44',
    }
    res = requests.get(
        'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid='+str(uid), headers=header)
    res.encoding = 'utf-8'
    js = json.loads(res.text)
    print('getLiveStatusbyUID')
    print(js)
    if js['code'] == 0 and js['data']['roomStatus'] == 1:
        return js['data']
    else:
        return {}


# 根据uid查询用户信息
def getUserInfobyUID(uid: str) -> {}:
    res = requests.get('https://api.bilibili.com/x/space/acc/info?mid='+str(uid))
    res.encoding = 'utf-8'
    js = json.loads(res.text)
    print('getUserInfobyUID')
    print(js)
    if js['code'] == 0:
        return js['data']
    else:
        return {}
