# -*-coding:utf8-*-
from nonebot import on_command, CommandSession
from .data_source import rollCard, dice, diceN

__plugin_name__ = 'coc'
__plugin_usage__ = r"功能列表:\n人物车卡: .coc .车卡\n指定骰点: .roll .r(格式为.r x1dy1+x2dy2+...+z)\n技能检定: .check .c(格式为.c 技能名 技能等级)\n理智检定: .sancheck .c(格式为.sc 意志 成功掉san/失败掉san)"


@on_command('coc', aliases=('车卡'), only_to_me=False)
async def makeCard(session: CommandSession):
    card = await rollCard()
    for msg in card:
        await session.send(msg)


@on_command('roll', only_to_me=False)
async def rollpoint(session: CommandSession):
    maxpoint = 100
    reg = session.current_arg_text.strip()
    if reg:
        print(reg)
        if reg.isdigit():
            print('is digit')
            maxpoint = int(reg)
            if maxpoint < 1:
                await session.send('爬.')
                return
        else:
            print('not digit')
            await session.send('格式错误,请输入正整数或留空(默认100).')
            return

    result = dice(maxpoint)
    user = session.ctx['sender']['nickname']
    # await session.send(str(session.ctx))
    await session.send('%sroll出了%d库啵.' % (user, result))


@on_command('r', only_to_me=False)
async def rollcomplex(session: CommandSession):
    reg = session.current_arg_text.strip()
    if not reg:
        await session.send('未输入计算式')
    # base_reg = reg.split("+")
    # reg,sum = roll()

    await session.send('你roll出了10000')


@on_command('check', aliases=('检定'), only_to_me=False)
async def check(session: CommandSession):
    reg = session.current_arg_text.strip()
    user = session.ctx['sender']['nickname']
    if not reg:
        await session.send('未输入参数,格式为.check/.检定 技能名 技能等级')
        return
    skill = reg.split(" ")
    if len(skill) == 2 and skill[1].isdigit():
        skill_lv = int(skill[1])
        point = dice(100)
        if point == 1:
            await session.send('%s的%s技能获得了大成功,效果拔群.' % (user, skill[0]))
        elif point <= skill_lv / 5:
            await session.send('%s的%s技能获得了极难成功(%d),效果喜人.' % (user, skill[0], point))
        elif point <= skill_lv / 2:
            await session.send('%s的%s技能获得了困难成功(%d),效果不错.' % (user, skill[0], point))
        elif point <= skill_lv:
            await session.send('%s的%s技能使用成功(%d),可喜可贺.' % (user, skill[0], point))
        elif point > skill_lv:
            if skill_lv < 50 and point >= 96:
                await session.send('%s的%s技能大失败了(%d),一定是技能等级太低的问题.' % (user, skill[0], point))
            elif skill_lv > 50 and point == 100:
                await session.send('%s的%s技能大失败了(%d),那可真蠢.' % (user, skill[0], point))
            else:
                await session.send('%s的%s技能失败了(%d),令人遗憾.' % (user, skill[0], point))
    else:
        await session.send('参数格式错误,格式为.check/.检定 技能名 技能等级')
        return
    # await session.send('你的'+skill[0]+'等级为'+skill[1])


@on_command('sancheck', aliases=('sc'), only_to_me=False)
async def sancheck(session: CommandSession):
    # await session.send('你失去了100san,疯掉了.')
    reg = session.current_arg_text.strip()
    user = session.ctx['sender']['nickname']
    if not reg:
        await session.send('未输入参数,格式为.sancheck/.sc 当前san值')
        return
    if reg.isdigit():
        skill_lv = int(reg)
        point = dice(100)
        if point <= skill_lv:
            await session.send('%s的san check成功通过(%d),令人遗憾.' % (user, point))
        else:
            await session.send('%s的san check失败了(%d).' % (user, point))
    else:
        await session.send('参数格式错误,格式为.sancheck/.sc 当前san值')
        return


# 心理学
@on_command('心理学', only_to_me=False)
async def think(session: CommandSession):
    reg = session.ctx['raw_message'].strip().split(' ')
    if len(reg) != 2:
        print(session.ctx['raw_message'])
        await session.send('你要对谁过心理学?(格式:.心理学 目标)')
        # await session.send(session.ctx)
        return
    rnd = dice(100)
    user = session.ctx['sender']['nickname']
    msg = ''
    if rnd == 1:
        msg += '%s认为%s说的宛若人间真理,信服的鼓起了掌.' % (user, reg[1])
    elif rnd > 1 and rnd <= 10:
        msg += '%s认为%s说的很有道理,不应质疑.' % (user, reg[1])
    elif rnd > 10 and rnd <= 50:
        msg += '%s认为%s说的没有问题.' % (user, reg[1])
    elif rnd > 50 and rnd <= 90:
        msg += '%s认为%s在一派胡言.' % (user, reg[1])
    elif rnd > 90 and rnd <= 99:
        msg += '%s认为%s说的狗屁不通.' % (user, reg[1])
    elif rnd == 100:
        msg += '%s仿佛听到%s说了天底下最大的笑话,并笑出了声.' % (user, reg[1])
    await session.send(msg)
