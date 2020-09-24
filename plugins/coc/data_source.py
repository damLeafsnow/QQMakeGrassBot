import random
tg = [-2, -1, 0, 1, 2]
dmg = ['-2', '-1', '0', '1d4', '1d6']


async def rollCard() -> []:
    card = []
    attribute = '人物属性:\n'
    # roll str
    d1 = d6()
    d2 = d6()
    d3 = d6()
    Strength = (d1+d2+d3)*5
    attribute += '力量:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, Strength, '')
    # roll con
    d1 = d6()
    d2 = d6()
    d3 = d6()
    CON = (d1+d2+d3)*5
    attribute += '体质:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, CON, '')
    # roll siz
    d1 = d6()
    d2 = d6()
    d3 = 6
    SIZ = (d1+d2+d3)*5
    attribute += '体型:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, SIZ, '')
    # roll agi
    d1 = d6()
    d2 = d6()
    d3 = d6()
    Agility = (d1+d2+d3)*5
    attribute += '敏捷:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, Agility, '')
    # roll app
    d1 = d6()
    d2 = d6()
    d3 = d6()
    APP = (d1+d2+d3)*5
    attribute += '外貌:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, APP, '')
    # roll int
    d1 = d6()
    d2 = d6()
    d3 = 6
    Int = (d1+d2+d3)*5
    attribute += '智力:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, Int, '')
    # roll pow
    d1 = d6()
    d2 = d6()
    d3 = d6()
    POW = (d1+d2+d3)*5
    attribute += '意志:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, POW, '')
    # roll edu
    d1 = d6()
    d2 = d6()
    d3 = 6
    EDU = (d1+d2+d3)*5
    attribute += '教育:(%d+%d+%d)*5=%d,%s\n' % (d1, d2, d3, EDU, '')
    # roll luck
    d1 = d6()
    d2 = d6()
    d3 = d6()
    LUK = (d1+d2+d3)*5
    attribute += '幸运:(%d+%d+%d)*5=%d,%s' % (d1, d2, d3, LUK, '')
    card.append(attribute)
    ability = '基本能力:\n'
    temp = Strength+SIZ
    i = 0
    if temp in range(2, 65):
        i = 0
    elif temp in range(65, 85):
        i = 1
    elif temp in range(85, 125):
        i = 2
    elif temp in range(125, 165):
        i = 3
    elif temp in range(165, 205):
        i = 4
    ability += 'HP:%d\nMP:%d\n体格:%d\nSAN:%d\n' % (
        int((CON+SIZ)/10), POW/5, tg[i], POW)
    ability += '闪避:%d\n伤害加值:%s\n兴趣技能点:%d\n母语:%d' % (
        Agility/2, dmg[i], Int*2, EDU)
    card.append(ability)
    return card


def d6() -> int:
    return random.randint(1, 6)


def dice(maxpoint: int) -> int:
    return random.randint(1, maxpoint)


def diceN(times: int, maxpoint: int) -> []:
    answer = []
    for i in range(times):
        answer.append(random.randint(1, maxpoint))
    return answer


# def roll(x: int, y: int) -> (str, int):
#     res = '( '
#     sum = 0
#     for i in range(0, x):
#         d = random.randint(1, y)
#         res += d+' '
#         sum += d
#     res += ')'
#     return res, sum
