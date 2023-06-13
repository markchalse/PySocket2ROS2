from Socket2Ros import Socket2Ros
import random 
import time
from CommandSys import COMMAND_CODE

def walk(msg):
    print (' i am walking ! ')

sr = Socket2Ros("127.0.0.1")
sr.command.add_command_handle(COMMAND_CODE['walk'],walk)
while True:
    sr.send_socket_msg(str(random.random()))
    time.sleep(10)
    

