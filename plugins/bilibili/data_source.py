import urllib.request
from urllib.request import urlopen
import requests
import sys
import ssl
import importlib
import json
importlib.reload(sys)

def get_bilibili_info(bvid: str) -> []:
    res = requests.get('http://api.bilibili.com/x/web-interface/view?bvid='+str(bvid))
    res.encoding='utf-8'
    res = res.text
    info = json.loads(res)
    data = info['data']
    owner = data['owner']
    info = []
    info.append('标题:'+data['title']+'UP主:'+owner['name']+'\n简介:'+data['desc']+'\n分类:'+data['tname']+'\n')
    info.append('[CQ:image,file='+data['pic']+']')
    info.append('视频链接:\nhttps://www.bilibili.com/video/'+bvid+'\n\nhttps://www.bilibili.com/video/av'+str(data['aid']))
    return info