from urllib.request import urlopen
import requests
import json
from bs4 import BeautifulSoup
import re

def get_bilibili_info_by_avid(avid: str) -> []:
    res = requests.get('https://api.bilibili.com/x/web-interface/view?aid='+str(avid))
    res.encoding='utf-8'
    res = res.text
    info = json.loads(res)
    if info['code'] != 0: #解析错误
        return []
    
    data = info['data']
    owner = data['owner']
    info = []
    info.append('标题:'+data['title']+'UP主:'+owner['name']+'\n简介:'+data['desc']+'\n分类:'+data['tname']+'\n')
    info.append('[CQ:image,file='+data['pic']+']')
    info.append('视频链接:\nhttps://www.bilibili.com/video/'+data['bvid']+'\n\nhttps://www.bilibili.com/video/av'+str(data['aid']))
    return info

def get_bilibili_info_by_bvid(bvid: str) -> []:
    res = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+str(bvid))
    res.encoding='utf-8'
    res = res.text
    info = json.loads(res)
    if info['code'] != 0: #解析错误
        return []
    
    data = info['data']
    owner = data['owner']
    info = []
    info.append('标题:'+data['title']+'UP主:'+owner['name']+'\n简介:'+data['desc']+'\n分类:'+data['tname']+'\n')
    info.append('[CQ:image,file='+data['pic']+']')
    info.append('视频链接:\nhttps://www.bilibili.com/video/'+data['bvid']+'\n\nhttps://www.bilibili.com/video/av'+str(data['aid']))
    return info

def get_bilibili_info_by_b23tv(b23str: str) -> []:
    res = requests.get('https://b23.tv/'+b23str)
    res.encoding='utf-8'
    soup = BeautifulSoup(res.text, 'html.parser')
    for tag in soup.find_all(re.compile("^meta")):
        if tag['content'].startswith('https://www.bilibili.com/video/av'):
            vid = tag['content'].split('/')[-2][2:]
            return get_bilibili_info_by_avid(vid)