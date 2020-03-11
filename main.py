import sys
import time
import os

try :
  impoort flask
except ModuleNotfoundError:
  print('正在安装必须的模块，请稍后...')
  os.system('pip install -r requirements')
  
# 检测所安装python的版本
__MAJOR, __MINOR, __MICRO = sys.version_info[0], sys.version_info[1], sys.version_info[2]
if __MAJOR < 3:
    print('Python版本号过低，当前版本为 %d.%d.%d， 请重装Python解释器' % (__MAJOR, __MINOR, __MICRO))
    time.sleep(2)
    exit()
    
if __name__ == "__main__":
    from wechat_robot import app
    print('正在打开服务器...')
    app.run(host='0.0.0.0', port=80, debug=True)
