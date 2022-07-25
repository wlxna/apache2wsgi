import sys 
import logging 
import os
logging.basicConfig(stream=sys.stderr)
# 添加项目运行虚拟环境，把第三步执行的虚拟环境地址放入以下
sys.path.append("/var/www/envPython3.8/lib/python3.8/site-packages")
os.path.join(os.path.dirname(__file__), 'templates/')
# 添加项目
sys.path.insert(0,"/var/www/xxq/")
# 添加app，这里main是我flask的入口文件，app是flask的程序名称：app = Flask(__name__)
from server import app as application
