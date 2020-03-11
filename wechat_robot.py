from config import TOKEN,XML_STR
from flask import Flask, request, make_response
import hashlib
import xml.etree.ElementTree as ET
from weather import get_weather
from joke import get_joke

app = Flask(__name__)  # 实例化一个Flask app

@app.route('/message', methods=['GET', 'POST'])  # 路由请求有get post两种
def chatme():  # 定义控制器函数gf
    if request.method == 'GET':  # GET请求
        data = request.args  # 获取GET请求的参数
        token = TOKEN  # 微信接口调用的token
        signature = data.get('signature', '')  # 微信接口调用的签名
        timestamp = data.get('timestamp', '')  # 微信接口相关时间戳参数
        nonce = data.get('nonce', '')  # 微信接口相关nonce参数
        echostr = data.get('echostr', '')  # 微信接口相关echostr参数
        s = [timestamp, nonce, token]
        s = ''.join(s).encode("utf-8")  # 连接字符串用来校验签名

        if hashlib.sha1(s).hexdigest() == signature:  # 校验签名
            return make_response(echostr)

        else:  # 响应签名错误
            return make_response("signature validation error")
    if request.method == 'POST':
        xml_str = request.stream.read()
        xml = ET.fromstring(xml_str)
        toUserName = xml.find('ToUserName').text
        fromUserName = xml.find('FromUserName').text
        createTime = xml.find('CreateTime').text
        msgType = xml.find('MsgType').text
        # 判断是否文本消息
        if msgType != 'text':
            reply = XML_STR % (
                fromUserName,
                toUserName,
                createTime,
                'text',
                'Unknow Format, Please check out'
            )
            return reply
        content = xml.find('Content').text
        msgId = xml.find('MsgId').text
        if u'笑话' in content:               # 输出笑话
            content = get_joke()
        elif content[-2:] == "天气":        # 输出天气
            keyword = content[:-2]
            if len(keyword) < 2:
                content = '请输入正确的城市名称'
                return XML_STR % (fromUserName, toUserName, createTime, msgType, content)
            content = get_weather(keyword)
        else:
            # 输出反话
            if type(content).__name__ == "unicode":
                content = content[::-1]
                content = content.encode('UTF-8')
            elif type(content).__name__ == "str":
                print(type(content).__name__)
                content = content
                content = content[::-1]

        # 返回xml文件
        reply = XML_STR % (fromUserName, toUserName, createTime, msgType, content)
        return reply

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8000, debug=True)
