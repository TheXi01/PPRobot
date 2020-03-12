'''
开始
->发送网络请求（应用：requests.get()）
->解析页面代码(应用：Xpath（）方法)
->遍历数据（for循环）
->随机获取一条数据（应用：random.randint()方法）
->结束
random.randint(a.b)在a和b区间内获取一个随机数
xpath('string(.)')string(.)可以用于提取标签嵌套标签的内容。
'''
import requests
from lxml import etree
from random import randint

def get_joke():
    url="http://www.lovehhy.net/Joke/Detail/QSBK/"+ str(randint(1, 100))
    r = requests.get(url)
    tree = etree.HTML(r.text)
    contentlist = tree.xpath('//div[@id="endtext"]')
    jokes = []

    for content in contentlist:
        content = content.xpath('string(.)')  # string() 函数将所有子文本串联起来，# 必须传递单个节点，而不是节点集。
        if '来源：' in content:  # 忽略包含“来源”笑话
            continue
        jokes.append(content)
    joke = jokes[randint(1, len(jokes))].strip()
    return joke

if __name__ == "__main__":
    content = get_joke()
    print(content)
