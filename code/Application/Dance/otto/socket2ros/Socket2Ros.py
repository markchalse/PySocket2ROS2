import socket
#import threading
import _thread
#from CommandSys import COMMAND_CODE
#import CommandSys.CommandSys

MAX_MSG_SIZE = 1024

class Socket2Ros:
    def __init__(self,CommandSys,server_ip,server_port=6000):
        self.command = CommandSys()
        #print (self.command.haddle_dict)
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client.connect((server_ip, server_port))
            self.start()
        except Exception as e:
            print (e)
    
    def send_socket_msg(self,msg):
        print ("send msg:%s"%msg)
        self.client.send(msg.encode('utf-8'))
        
    def get_socket_msg(self):
        while True:
            msg = self.client.recv(MAX_MSG_SIZE)
            if msg is not None:
                msg = msg.decode('utf-8')
                print ("server: %s"%msg)
                try:
                    msg_reply = self.command.parser_msg(msg)
                    if msg_reply!=None:
                        self.send_socket_msg(msg_reply)
                except Exception as e:
                    print (e)
    
            
    def start(self):
        _thread.start_new_thread(self.get_socket_msg,())
        #self.listen_thread = threading.Thread(target=self.get_socket_msg)
        #self.listen_thread.setDaemon(True)
        #self.listen_thread.start()
        
    def subscription_topic(self,topic_name):
        self.send_socket_msg(self.command.subscription_topic_request(topic_name))
        
    def create_publisher(self,topic_name):
        self.send_socket_msg(self.command.create_publisher_request(topic_name))
        
    def socket2ros_topic_publish(self,topic_name,msg_str):
        self.send_socket_msg(self.command.get_publish_topic_command(topic_name,msg_str))