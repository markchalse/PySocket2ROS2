

0
上传socket2ros文件夹到 otto的 /

1

需要连接server 的wifi  需要自动获取ip
修改rklib.network.py
connect_router() 
让他return sta_if.ifconfig()

2
main.py中加入连接server端wifi，并获取ip
ifconfig = connect_router(secrets["ssid"], secrets["password"]) 
将ip信息传递到ottoserver中：OTTOServer.start(ifconfig)


3
secrets.py中配置wifi密码

4 

OTTOServer.py

from socket2ros.Socket2Ros import Socket2Ros
from socket2ros.CommandSys import COMMAND_CODE
from socket2ros.CommandSys import CommandSys
import json

在start获得ip信息
@staticmethod
    def start(ifconfig):


定义socket通信客户端和回调函数
        sr = Socket2Ros(CommandSys,ifconfig[2])
        print ("sr init over")
        sr.command.add_command_handle(COMMAND_CODE['socket_pass_msg'],Socket2RosAction)
        #sr.subscription_topic("test_ros_topic")
        sr.subscription_topic("test_dance")


def Socket2RosAction(msg):
    msg_dict = json.loads(msg)
    act = msg_dict["data"]
    print ("action:",act)
    if act == "walkfoward":
        Otto.walk(2, 600, 1)
    if act == "walkback":
        Otto.walk(2, 600, -1)
    if act == "handsup":
        Otto.handsup()
    if act == "turn_left":
        Otto.turn(2, 1000, 1)
    if act == "turn_right":
        Otto.turn(2, 1000, -1)
    if act == "handwave_left":
        Otto.handwave(1)
    if act == "handwave_right":
        Otto.handwave(-1)
    if act == "shakelegleft":
        Otto.shakeLeg(1, 1000, 1)
    if act == "shakelegright":
        Otto.shakeLeg(1, 1000, -1)
    

