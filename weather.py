'''
开始->发送网络请求（request.get()）
->解析页面代码(Xpath()方法)
->组织数据（format（）方法）->获取天气数据(xpath.text()方法）
->结束
'''
import requests
from lxml import etree

def get_weather(keyword):
    url = 'https://www.tianqi.com/tianqi/search?keyword=' + keyword
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    tree = etree.HTML(response.text)
    # 检测城市天气是否存在
    try:
        city_name = tree.xpath('//dd[@class="name"]/h2/text()')[0]
    except:
        content = '没有该城市天气信息，请确认查询格式'
        return content
    week = tree.xpath('//dd[@class="week"]/text()')[0]
    now = tree.xpath('//p[@class="now"]')[0].xpath('string(.)')
    temp = tree.xpath('//dd[@class="weather"]/span')[0].xpath('string(.)')
    shidu = tree.xpath('//dd[@class="shidu"]/b/text()')
    kongqi = tree.xpath('//dd[@class="kongqi"]/h5/text()')[0]
    pm = tree.xpath('//dd[@class="kongqi"]/h6/text()')[0]
    content = "【{0}】{1}天气\n当前温度：{2}\n今日天气：{3}\n{4}\n{5}\n{6}".format(city_name, week.split('\u3000')[0], now, temp, '\n'.join(shidu),kongqi,pm)
    return content

if __name__ == "__main__":
    keyword = '哈尔滨'
    content = get_weather(keyword)
    print(content)