import socket
import threading
import sys                                                                  
import signal
import time
from socket2ros.CommandSys import CommandSys


MAX_MSG_SIZE = 1024


def quit(signum, frame):
    print ('stop fusion')
    sys.exit()

class Server2Ros:
    def __init__(self,port=6000):
        self.command = CommandSys()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0',port))
        self.clients = {}
        self.server.listen(5)
        print("server start, wait for client connecting...")
        
     
    def register(self,client,info,client_thread):
        client_id = str(info[0])+str(info[1])
        self.clients[client_id]={
            "client_id":client_id,
            "client":client,
            "info":info,
            "client_thread":client_thread
        }
        
    def start(self):
        self.accept_thread = threading.Thread(target=self.accept_client)
        self.accept_thread.setDaemon(True)
        self.accept_thread.start()
        
        self.heartbeat_thread = threading.Thread(target=self.heart_beat_check)
        self.heartbeat_thread.setDaemon(True)
        self.heartbeat_thread.start()
         
    def accept_client(self):
        while True:
            client, info = self.server.accept()
            print ("accept :",info)
            client_thread = threading.Thread(target=self.handle_socket_msg, args=(client, info))
            client_thread.setDaemon(True)
            client_thread.start() 
            self.register(client, info , client_thread)
        
    def send_socket_msg(self,client,info,msg):
        print ("send msg to %s %s :%s"%(str(info[0]),str(info[1]),msg))
        client.send(msg.encode('utf-8'))
        
    def get_socket_msg(self,client,info):
        msg = client.recv(MAX_MSG_SIZE)
        if msg is not None:
            msg = msg.decode('utf-8')
            print ("%s %s say: %s"%(str(info[0]),str(info[1]),msg))
            return msg
    
    def handle_socket_msg(self,client,info):
        while True:
            msg = self.get_socket_msg(client,info)
            msg_reply = self.command.parser_msg(msg)
            if msg_reply!=None:
                self.send_socket_msg(client,info,str(msg_reply))
    
    def heart_beat_check(self):
        while True:
            for client in self.clients.values():
                try:
                    self.send_socket_msg(client['client'],client['info'],self.command.get_heart_beat_request_command())
                except Exception as e:
                    print (e)
            time.sleep(15)

    
    def test_all_walk(self):
        for client in self.clients.values():
            try:
                self.send_socket_msg(client['client'],client['info'],self.command.get_walk_command())
            except Exception as e:
                print (e)
    
        

if __name__=="__main__":
    signal.signal(signal.SIGINT, quit)                                
    signal.signal(signal.SIGTERM, quit)
    
    SR = Server2Ros()
    SR.start()
    while True:
        time.sleep(10)
        SR.test_all_walk()