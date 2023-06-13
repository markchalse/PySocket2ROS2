import machine
import sys
from webserver import ESPWebServer
import ottolib.otto9 as otto9
from rklib.HCSR04 import HCSR04

from socket2ros.Socket2Ros import Socket2Ros
from socket2ros.CommandSys import COMMAND_CODE
from socket2ros.CommandSys import CommandSys
import json

import time

OTTO_ACTION = ""
#OTTO_ACTIN_TIME = int(time.strftime("%Y%m%d%H%M%S",time.localtime()))
ACTION_DELAY = 2

Otto = otto9.Otto9()

GPIO_NUM = 15  # Builtin led (Wemos S2 mini)
# Get pin object for controlling builtin LED
pin = machine.Pin(GPIO_NUM, machine.Pin.OUT)


# Handler for path "/cmd/home"
def handleHome(socket, args):
    Otto.home()
    ESPWebServer.ok(socket, "200", "home")
    print("home")


# Handler for path "/cmd/handsup"
def handleHandsUp(socket, args):
    Otto.handsup()
    ESPWebServer.ok(socket, "200", "handsup")


# Handler for path "/cmd/handwave?direction=[1|-1]"
def handleHandWave(socket, args):
    Otto.handwave(int(args['direction']))
    ESPWebServer.ok(socket, "200", "handwave")


# Handler for path "/cmd/jump?steps=[1,10]&period=[600,1400]"
def handleJump(socket, args):
    Otto.jump(int(args['steps']), int(args['period']))
    ESPWebServer.ok(socket, "200", "jump")


# Handler for path "/cmd/walk?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleWalk(socket, args):
    Otto.walk(int(args['steps']), int(args['period']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "walk")


# Handler for path "/cmd/turn?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleTurn(socket, args):
    Otto.turn(int(args['steps']), int(args['period']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "turn")


# Handler for path "/cmd/bend?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleBend(socket, args):
    Otto.bend(int(args['steps']), int(args['period']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "bend")


# Handler for path "/cmd/shakeLeg?steps=[1,10]&period=[600,1400]&direction=[1|-1]"
def handleShakeLeg(socket, args):
    Otto.shakeLeg(int(args['steps']), int(args['period']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "shakeLeg")


# Handler for path "/cmd/moonwalker?steps=[1,10]&period=[600,1400]&height=[15,40]&direction=[1|-1]"
def handleMoonwalker(socket, args):
    Otto.moonwalker(int(args['steps']), int(args['period']), int(args['height']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "moonwalker")


# Handler for path "/cmd/crusaito?steps=[1,10]&period=[600,1400]&height=[20,50]&direction=[1|-1]"
def handleCrusaito(socket, args):
    Otto.crusaito(int(args['steps']), int(args['period']), int(args['height']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "crusaito")


# Handler for path "/cmd/flapping?steps=[1,10]&period=[600,1400]&height=[10,30]&direction=[1|-1]"
def handleFlapping(socket, args):
    Otto.flapping(int(args['steps']), int(args['period']), int(args['height']), int(args['direction']))
    ESPWebServer.ok(socket, "200", "flapping")


# Handler for path "/cmd/updown?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleUpdown(socket, args):
    Otto.updown(int(args['steps']), int(args['period']), int(args['height']))
    ESPWebServer.ok(socket, "200", "shakeLeg")


# Handler for path "/cmd/swing?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleSwing(socket, args):
    Otto.swing(int(args['steps']), int(args['period']), int(args['height']))
    ESPWebServer.ok(socket, "200", "shakeLeg")


# Handler for path "/cmd/tiptoeSwing?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleTiptoeSwing(socket, args):
    Otto.tiptoeSwing(int(args['steps']), int(args['period']), int(args['height']))
    ESPWebServer.ok(socket, "200", "tiptoeSwing")


# Handler for path "/cmd/ascendingTurn?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleAscendingTurn(socket, args):
    Otto.ascendingTurn(int(args['steps']), int(args['period']), int(args['height']))
    ESPWebServer.ok(socket, "200", "ascendingTurn")


# Handler for path "/cmd/jitter?steps=[1,10]&period=[600,1400]&height=[0,90]"
def handleJitter(socket, args):
    Otto.jitter(int(args['steps']), int(args['period']), int(args['height']))
    ESPWebServer.ok(socket, "200", "jitter")


# Handler for path "/cmd/playGesture"
def handleGesture(socket, args):
    Otto.playGesture(int(args["gesture"]))
    ESPWebServer.ok(socket, "200", "playGesture")


# Handler for path "/cmd/saveTrims"
def handleSaveTrims(socket, args):
    Otto.setTrims(int(args["YL"]), int(args["YR"]), int(args["RL"]), int(args["RR"]), int(args["LA"]), int(args["RA"]))
    Otto.saveTrimsOnEEPROM()
    ESPWebServer.ok(socket, "200", "saveTrims")


from machine import Pin
import time
trig = Pin(5, Pin.OUT)
echo = Pin(18, Pin.IN)
HC = HCSR04(trig, echo)
ts = time.ticks_us()  # 上一次获取超声波时间

def modeHCSR():
    global ts
    te = time.ticks_us()  # 当前时间
    tc = te - ts
    if tc > 1000000:
        ts = te
        distance = HC.getDistance()
        print("distance",distance)
        if distance < 10: #<5cm, 后退一步
            print("<10cm, 后退一步")
            Otto.walk(1, int(1000), int(-1)) 

def Socket2RosAction(msg):
    #now = int(time.strftime("%Y%m%d%H%M%S",time.localtime()))
    #if now-OTTO_ACTIN_TIME>ACTION_DELAY:
    #    OTTO_ACTIN_TIME = now
    #else:
    #    return
    
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
    
    
class OTTOServer:
    def __init__(self):
        pass

    @staticmethod
    def setup():
#         Otto.initHUMANOID(39, 37, 35, 33, 18, 16, True, -1, -1, -1, -1)  # s2 mini + DIY IO shields pins
#         Otto.init(39, 37, 35, 33, True, -1, -1, -1, -1)  # s2 mini + DIY IO shields pins
        Otto.initHUMANOID(12, 11, 9, 7, 33, 35, True, -1, -1, -1, -1)  # s2 mini + IO shields pins
#         Otto.init(12, 11, 9, 7, True, -1, -1, -1, -1)  # s2 mini + IO shields pins
        Otto.home()

        # Start the server @ port 8899
        # ESPWebServer.begin(8899)
        ESPWebServer.begin()  # use default 80 port

        # Register handler for each path
        # ESPWebServer.onPath("/", handleRoot)
        ESPWebServer.onPath("/cmd/home", handleHome)
        ESPWebServer.onPath("/cmd/handsup", handleHandsUp)
        ESPWebServer.onPath("/cmd/jump", handleJump)
        ESPWebServer.onPath("/cmd/handwave", handleHandWave)

        ESPWebServer.onPath("/cmd/walk", handleWalk)
        ESPWebServer.onPath("/cmd/turn", handleTurn)

        ESPWebServer.onPath("/cmd/bend", handleBend)
        ESPWebServer.onPath("/cmd/shakeLeg", handleShakeLeg)
        ESPWebServer.onPath("/cmd/moonwalker", handleMoonwalker)
        ESPWebServer.onPath("/cmd/crusaito", handleCrusaito)
        ESPWebServer.onPath("/cmd/flapping", handleFlapping)

        ESPWebServer.onPath("/cmd/swing", handleSwing)
        ESPWebServer.onPath("/cmd/updown", handleUpdown)
        ESPWebServer.onPath("/cmd/tiptoeSwing", handleTiptoeSwing)
        ESPWebServer.onPath("/cmd/ascendingTurn", handleAscendingTurn)
        ESPWebServer.onPath("/cmd/jitter", handleJitter)

        ESPWebServer.onPath("/cmd/playGesture", handleGesture)

        ESPWebServer.onPath("/cmd/saveTrims", handleSaveTrims)

        # Setting the path to documents
        ESPWebServer.setDocPath("/webroot")

        # Setting maximum Body Content Size. Set to 0 to disable posting. Default: 1024
        ESPWebServer.setMaxContentLength(1024)


    @staticmethod
    def start(ifconfig):#markchalse
        pin.on()  # Turn LED off (it use sinking input)
        
        #markchalse
        sr = Socket2Ros(CommandSys,ifconfig[2])
        print ("sr init over")
        sr.command.add_command_handle(COMMAND_CODE['socket_pass_msg'],Socket2RosAction)
        #sr.subscription_topic("test_ros_topic")
        sr.subscription_topic("test_dance")

        try:
            while True:
                # Let server process requests
                ESPWebServer.handleClient()
                modeHCSR()
        except:
            pin.off()
#             OTTOServer.start()
            ESPWebServer.close()
