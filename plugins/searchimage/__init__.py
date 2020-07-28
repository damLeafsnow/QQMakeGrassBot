# -*-coding:utf8-*-
from nonebot import on_command, CommandSession
from .saucenaopy import SauceNAO


__plugin_name__ = 'searchimage'
__plugin_usage__ = r".搜图 搜索图片"


@on_command('搜图', only_to_me=False)
async def getimg(session: CommandSession):
    # reg = session.current_arg_text.strip()
    seq = session.current_arg_images[0]
    print(seq)
    aucenao = SauceNAO('29a2b59e2bc12b60603d8dc3b2dfafa144f40614')
    filtered_results = aucenao.get_sauce(seq)
    data = filtered_results['results'][0]['data']
    msg = '搜索结果:'
    if 'pixiv_id' in data:
        msg += '\ntitle:' + str(data['title'])
        msg += '\npixiv_id:' + str(data['pixiv_id'])
        msg += '\nmember_name:' + str(data['member_name'])
        msg += '\nmember_id:' + str(data['member_id'])
        msg += '\nurl:' + str(data['ext_urls'][0])
    elif 'source' in data:
        msg += '\ncreator:' + str(data['creator'])
        msg += '\nmaterial:' + str(data['material'])
        msg += '\ncharacters:' + str(data['characters'])
        msg += '\nsource:' + str(data['source'])
    else:
        msg += ''.join(data)
    await session.send(msg)
