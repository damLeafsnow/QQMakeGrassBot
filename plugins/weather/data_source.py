
import urllib.request
from urllib.request import urlopen
import requests
import sys
import ssl
import importlib
import json
importlib.reload(sys)

async def get_weather_of_city(city: str) -> str:
    host = 'http://wthrcdn.etouch.cn/weather_mini?city='
    url = host + urllib.parse.quote(city)
    r = requests.get(url)
    jsons = json.loads(r.text)
    res = city+'天气:\n'
    for i in jsons['data']['forecast']:
        res += i['date']+':天气'+i['type']+' 最'+i['low']+' 最'+i['high']+'\n'
    return res