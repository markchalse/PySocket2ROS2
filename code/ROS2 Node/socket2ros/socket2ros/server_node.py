import rclpy
from rclpy.node import Node
from std_msgs.msg import String

from .CommandSys import CommandSys
from .CommandSys import COMMAND_CODE
import socket
import threading
import sys
import threading
import time
import json


MAX_MSG_SIZE = 1024
EMPTY_MSG_CONTROL = 20
HEART_DEAD_MAX = 3

class SocketClientRosAgent():
    def __init__(self,client_id,client,topic_name):
        self.client_id = client_id
        self.client = client
        self.topic_name = topic_name
    
    def handle_msg(self,msg):
        msg= msg.data
        try:
            self.client.send(CommandSys().pack_command(COMMAND_CODE['socket_pass_msg'],msg).encode('utf-8'))
        except Exception as e:
            return
        print ("send topic=%s msg to %s  :%s"%(self.topic_name , self.client_id , msg))

class Server2Ros(Node):
    def __init__(self,port=6000):
        super().__init__('Server_Ros')
        self.command = CommandSys()
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind(('0.0.0.0',port))
        self.socket_clients = {}
        self.server.listen(5)
        self.publisher_dict = {}    
        print("server start, wait for client connecting...")
        self.start()

    def subscription_topic_for_client(self,topic_name,client_id):
        self.socket_clients[client_id]['listen_topic'][topic_name] = {}
        self.socket_clients[client_id]['listen_topic'][topic_name]['ros_agent'] = SocketClientRosAgent(client_id,self.socket_clients[client_id]['client'],topic_name)
        self.socket_clients[client_id]['listen_topic'][topic_name]['subscription'] = self.create_subscription(String,topic_name,self.socket_clients[client_id]['listen_topic'][topic_name]['ros_agent'].handle_msg,10)
    
    def create_publisher_for_client(self,topic_name,client_id):
        if topic_name not in self.publisher_dict.keys():
            self.publisher_dict[topic_name] = self.create_publisher(String, topic_name, 50)

    def socket_ros_topic_publisher(self,topic_name,client_id,msg_str):
        try:
            msg = String()
            msg.data = msg_str
            self.publisher_dict[topic_name].publish(msg)
        except Exception as e:
            print (e)
    
    def register(self,client,info,client_thread):
        client_id = str(info[0])+str(info[1])
        self.socket_clients[client_id]={
            "client_id":client_id,
            "client":client,
            "info":info,
            "client_thread":client_thread,
            "empy_msg_counter":0,
            "listen_topic":{},
            "publisher_topic":{},
            "heart_dead_num":0
        }
        
    def start(self):
        self.accept_thread = threading.Thread(target=self.accept_client)
        #self.accept_thread.setDaemon(True)#python2
        self.accept_thread.daemon=True #python3
        self.accept_thread.start()
        
        self.heartbeat_thread = threading.Thread(target=self.heart_beat_check)
        #self.heartbeat_thread.setDaemon(True)#python2
        self.heartbeat_thread.daemon = True#python3
        self.heartbeat_thread.start()
         
    def accept_client(self):
        while True:
            client, info = self.server.accept()
            print ("accept :",info)
            client_thread = threading.Thread(target=self.handle_socket_msg, args=(client, info))
            #client_thread.setDaemon(True)#python2
            client_thread.daemon = True#python3
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
            if len(msg)==0:
                self.socket_clients[str(info[0])+str(info[1])]['empy_msg_counter'] +=1
            else:
                self.socket_clients[str(info[0])+str(info[1])]['empy_msg_counter'] = 0
            if self.socket_clients[str(info[0])+str(info[1])]['empy_msg_counter'] > EMPTY_MSG_CONTROL:
                print ("--- listen thread close ---")
                break
            msg_reply = self.command.parser_msg(msg)
            if msg_reply!=None:
                reply_flag = True
                if json.loads(msg_reply)['code'] == COMMAND_CODE['subscription_topic_reply']:
                    self.subscription_topic_for_client(json.loads(msg)['data'],str(info[0])+str(info[1]))
                if json.loads(msg_reply)['code'] == COMMAND_CODE['create_publisher_reply']:
                    self.create_publisher_for_client(json.loads(msg)['data'],str(info[0])+str(info[1]))
                if json.loads(msg_reply)['code'] == COMMAND_CODE['publish_topic_reply']:
                    self.socket_ros_topic_publisher(json.loads(msg)['data']['topic_name'],str(info[0])+str(info[1]),json.loads(msg)['data']['msg_str'])
                if json.loads(msg_reply)['code'] == COMMAND_CODE['is_alive']:
                    self.socket_clients[str(info[0])+str(info[1])]['heart_dead_num'] = 0
                    reply_flag = False   
                if reply_flag:
                    self.send_socket_msg(client,info,str(msg_reply))
    
    def heart_beat_check(self):
        while True:
            for client_id in self.socket_clients.keys():
                if self.socket_clients[client_id]['heart_dead_num'] > HEART_DEAD_MAX:
                    print ("pop dead client :%s"%client_id)
                    self.socket_clients.pop(client_id)
                    break
                else:
                    try:
                        self.socket_clients[client_id]['heart_dead_num']+=1
                        self.send_socket_msg(self.socket_clients[client_id]['client'],self.socket_clients[client_id]['info'],self.command.get_heart_beat_request_command())
                    except Exception as e:
                        print (e)
            time.sleep(15)        

    def listener_callback(self, msg):
        self.get_logger().info('I heard: "%s"' % msg.data)

    def test_all_walk(self):
        for client in self.socket_clients.values():
            try:
                self.send_socket_msg(client['client'],client['info'],self.command.get_walk_command())
            except Exception as e:
                print (e)


def main(args=None):
    rclpy.init(args=args)
    my_node_model = Server2Ros()
    rclpy.spin(my_node_model)
    my_node_model.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
