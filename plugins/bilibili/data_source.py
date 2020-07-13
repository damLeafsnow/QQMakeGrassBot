from urllib.request import urlopen
import requests
import json
import time
from os import path, mkdir
from bs4 import BeautifulSoup
import re


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

# 用户uid 用户名列表索引


def GetDynamicStatus(uid, name, i):
    res = requests.get(
        'https://api.vc.bilibili.com/dynamic_svr/v1/dynamic_svr/space_history?host_uid='+str(uid)+'offset_dynamic_id=0')
    res.encoding = 'utf-8'
    res = res.text
    cards_data = json.loads(res)
    cards_data = cards_data['data']['cards']
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
                    name + '发了新专栏「' + cards_data[index]['card']['title'] + '」并说： ' + cards_data[index]['card']['dynamic'])
                imageurls = cards_data[index]['card']['image_urls']
                if imageurls:
                    for images in cards_data[index]['card']['image_urls']:
                        content_list.append('[CQ:image,file='+images+']')
            else:
                if (cards_data[index]['desc']['type'] == 8):
                    content_list.append(
                        name + '发了新视频「' + cards_data[index]['card']['title'] + '」并说： ' + cards_data[index]['card']['dynamic'])
                    content_list.append(
                        '[CQ:image,file='+cards_data[index]['card']['pic']+']')
                else:
                    if ('description' in cards_data[index]['card']['item']):
                        # 带图新动态
                        content_list.append(
                            name + '发了新动态： ' + cards_data[index]['card']['item']['description'])
                        # CQ使用参考：[CQ:image,file=http://i1.piimg.com/567571/fdd6e7b6d93f1ef0.jpg]
                        for pic_info in cards_data[index]['card']['item']['pictures']:
                            content_list.append(
                                '[CQ:image,file='+pic_info['img_src']+']')
                    else:
                        # 转发动态
                        if 'origin_user' in cards_data[index]['card']:
                            origin_name = cards_data[index]['card']['origin_user']['info']['uname']
                            content_list.append(
                                name + '转发了「' + origin_name + '」的动态并说： ' + cards_data[index]['card']['item']['content'])
                        else:
                            # 这个是不带图的自己发的动态
                            content_list.append(
                                name + '发了新动态： ' + cards_data[index]['card']['item']['content'])
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


def GetLiveStatus(uid, name, i):
    res = requests.get(
        'https://api.live.bilibili.com/room/v1/Room/getRoomInfoOld?mid='+str(uid))
    res.encoding = 'utf-8'
    res = res.text
    try:
        with open('./dynamics/'+str(uid)+'_'+str(i)+'Live', 'r') as f:
            last_live_str = f.read()
            f.close()
    except Exception as err:
        last_live_str = '0'
        print(err)
    live_data = json.loads(res)
    live_data = live_data['data']
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
            live_msg.append(name + '直播中:' + live_title)
            live_msg.append('[CQ:image,file='+live_cover+']')
            live_msg.append('直播地址:'+live_url+'\n当前观看人数:'+live_watcher)
            return live_msg
    return ''
