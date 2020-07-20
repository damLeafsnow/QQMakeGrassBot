import sys
import imp
from os import path, mkdir
# from datetime import datetime, timedelta
from pixivpy3 import bapi
import requests
import random

imp.reload(sys)
sys.dont_write_bytecode = True


def searchByTag(tag: str) -> []:
    # 检查图片存放路径
    if not path.exists('./pixdata/'):
        mkdir('./pixdata')

    api = bapi.ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    api.require_appapi_hosts()
    api.set_accept_language('en-us')

    account = []
    try:
        with open('./datas/PIXIV_Account', "r", encoding="utf-8") as f:
            for line in f:
                str_t = str(line).strip()  # 清理/n和空格
                account.append(str_t)
            f.close()
            print(account)
    except Exception as err:
        print(err)

    api.login(account[0], account[1])

    # 标签搜索
    json_result = api.search_illust(
        tag, search_target='partial_match_for_tags')
    if not json_result.illusts:
        return []

    ill = []
    illust = json_result.illusts[0]
    msg = str('标题: ' + str(illust.title) + '\n标签: ')
    for tag in illust.tags:
        msg += '%s(%s)  ' % (tag['name'], tag['translated_name'])
    # msg += '\n简介: ' + str(illust.caption)
    msg += "\n链接: https://www.pixiv.net/artworks/" + str(illust.id)
    ill.append(msg)

    if illust.meta_single_page:
        url = illust.image_urls.medium
        # url = illust.meta_single_page.original_image_url
        api.download(url, path='./pixdata/',
                     name=str(0)+str(url)[-4:], replace=True)
        ill.append('\\pixdata\\0%s' % str(url)[-4:])
        # '[CQ:image,file='+str('/pixdata/0%s' % str(url)[-4:])+']')
    elif illust.meta_pages:
        i = 0
        for meta_page in illust.meta_pages:
            url = meta_page.image_urls.medium
            api.download(url, path='./pixdata/',
                         name=str(i)+str(url)[-4:], replace=True)
            ill.append('\\pixdata\\%d%s' % (i, str(url)[-4:]))
            # '[CQ:image,file='+str('/pixdata/%d%s'
            #   % (i, str(url)[-4:]))+']')
            i += 1

    return ill


def getPic():
    if random.randint(1, 2) == 1:
        res = requests.get("http://api.mtyqx.cn/api/random.php", verify=False)
    else:
        res = requests.get("http://www.dmoe.cc/random.php", verify=False)

    # 保存图片
    with open('./pixdata/x.png', "wb") as f:
        f.write(res.content)
    return True
