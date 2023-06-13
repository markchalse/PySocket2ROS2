# import tests.led_test

from secrets import secrets, ap
from rklib.network import connect_router, setup_ap
ifconfig = connect_router(secrets["ssid"], secrets["password"]) #markchalse
#connect_router(secrets["ssid"], secrets["password"])
#setup_ap(ap["ssid"], ap["password"])


from OTTOServer import OTTOServer

OTTOServer.setup()
OTTOServer.start(ifconfig)#markchalse
