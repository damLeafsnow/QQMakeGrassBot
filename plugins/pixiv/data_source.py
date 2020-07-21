import sys
import imp
from os import path, mkdir
# from datetime import datetime, timedelta
# from pixivpy3 import bapi
import requests
import random

imp.reload(sys)
sys.dont_write_bytecode = True

# 切换为第三方api


def searchByTag(tag: str, num: int, pages: int, Bookmarks: int) -> []:
    header = {
        'Referer': 'https://pixivic.com/popSearch',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.116 Safari/537.36'
    }

    # 返回数据
    result_datas = []
    index = 0

    for i in range(1, pages+1):
        param = {
            'keyword': tag,
            'page': i
        }
        url = 'https://api.pixivic.com/illustrations'
        s = requests.get(url, headers=header, params=param)
        json_result = s.json()
        # if(json_result['message'] == '搜索结果获取成功'):
        if 'data' in json_result:
            print('第%d页搜索结果获取成功' % i)
        else:
            return result_datas
        img_datas = json_result['data']

        # 页内所有图片
        for data in img_datas:
            # 找够图返回
            print('已下载图片%d,总图库%d' % (index, len(result_datas)))
            if len(result_datas) == num:
                return result_datas
            # 收藏数小于阈值跳过
            if 'totalBookmarks' not in data:
                continue
            if data['totalBookmarks'] < Bookmarks:
                continue

            # 图片信息
            img = []
            img_data = '标题: ' + data['title']
            img_data += '\n画师: ' + data['artistPreView']['name'] + \
                '(' + 'https://www.pixiv.net/users/' + \
                str(data['artistPreView']['id']) + ')'
            img_data += '\n标签: '
            for tag in data['tags']:
                img_data += '%s%s  ' % (tag['name'],
                                        '' if tag['translatedName'] == ''
                                        else '('+tag['translatedName']+')')
            img_data += '\n链接: https://www.pixiv.net/artworks/' + \
                str(data['id'])
            img_data += '\n图片格式:%d*%d,上传日期:%s' % (
                data['width'], data['height'], data['createDate'])
            img_data += '\n浏览次数:%d,收藏数:%d' % (
                data['totalView'], data['totalBookmarks'])
            img.append(img_data)

            # 图片链接
            max = 5  # 防止有大量图的图库
            for image in data['imageUrls']:
                if max == 0:
                    break
                img_url = image['medium']
                img_url = img_url.replace(
                    'i.pximg.net', 'img.cheerfun.dev:233')
                if not path.exists('./pixdata/'):
                    mkdir('./pixdata')
                filename = '%d%s' % (index, img_url[-4:])
                print(filename)
                try:
                    res = requests.get(img_url, headers=header)
                except requests.RequestException:
                    print('图片下载错误')
                    return []
                with open('./pixdata/'+filename, "wb") as f:
                    f.write(res.content)
                img.append(filename)
                index += 1
                max -= 1
            result_datas.append(img)
    return result_datas

    # # 检查图片存放路径
    # if not path.exists('./pixdata/'):
    #     mkdir('./pixdata')

    # api = bapi.ByPassSniApi()  # Same as AppPixivAPI, but bypass the GFW
    # api.require_appapi_hosts()
    # api.set_accept_language('en-us')

    # account = []
    # try:
    #     with open('./datas/PIXIV_Account', "r", encoding="utf-8") as f:
    #         for line in f:
    #             str_t = str(line).strip()  # 清理/n和空格
    #             account.append(str_t)
    #         f.close()
    #         print(account)
    # except Exception as err:
    #     print(err)

    # api.login(account[0], account[1])

    # # 标签搜索
    # json_result = api.search_illust(
    #     tag, search_target='partial_match_for_tags')
    # if not json_result.illusts:
    #     return []

    # ill = []
    # illust = json_result.illusts[0]
    # msg = str('标题: ' + str(illust.title) + '\n标签: ')
    # for tag in illust.tags:
    #     msg += '%s(%s)  ' % (tag['name'], tag['translated_name'])
    # # msg += '\n简介: ' + str(illust.caption)
    # msg += "\n链接: https://www.pixiv.net/artworks/" + str(illust.id)
    # ill.append(msg)

    # if illust.meta_single_page:
    #     url = illust.image_urls.medium
    #     # url = illust.meta_single_page.original_image_url
    #     api.download(url, path='./pixdata/',
    #                  name=str(0)+str(url)[-4:], replace=True)
    #     ill.append('\\pixdata\\0%s' % str(url)[-4:])
    #     # '[CQ:image,file='+str('/pixdata/0%s' % str(url)[-4:])+']')
    # elif illust.meta_pages:
    #     i = 0
    #     for meta_page in illust.meta_pages:
    #         url = meta_page.image_urls.medium
    #         api.download(url, path='./pixdata/',
    #                      name=str(i)+str(url)[-4:], replace=True)
    #         ill.append('\\pixdata\\%d%s' % (i, str(url)[-4:]))
    #         # '[CQ:image,file='+str('/pixdata/%d%s'
    #         #   % (i, str(url)[-4:]))+']')
    #         i += 1

    # return ill


def getPic():
    i = random.randint(1, 2)
    print(i)
    if i == 1:
        res = requests.get("http://api.mtyqx.cn/api/random.php", verify=False)
    elif i == 2:
        res = requests.get("http://www.dmoe.cc/random.php", verify=False)
    # elif i == 3:
        # res = requests.get("https://random.52ecy.cn/randbg.php", verify=False)
    # elif i == 3:
        # res = requests.get("http://img.xjh.me/random_img.php", verify=False)

    # 检查图片存放路径
    if not path.exists('./pixdata/'):
        mkdir('./pixdata')
    # 保存图片
    with open('./pixdata/x.png', "wb") as f:
        f.write(res.content)
        f.close()
    return True
