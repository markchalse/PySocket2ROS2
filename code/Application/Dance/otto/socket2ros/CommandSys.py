import json

COMMAND_CODE={
    'heartbeat_request':'100',
    'heartbeat_reply':'101',
    'walk':'201',
    'subscription_topic':'300',
    'subscription_topic_reply':'301',
    'create_publisher':'400',
    'create_publisher_reply':'401',
    'publish_topic':'402',
    'publish_topic_reply':'403',
    'socket_pass_msg':'501'
}

class CommandSys:
    def __init__(self):
        self.haddle_dict = {
            '100':self.heartbeat_request,
            '101':self.heartbeat_reply,
            '300':self.subscription_topic,
            '400':self.create_publisher,
            '402':self.publish_topic
        }
    
    def pack_command(self,code,data=None):
        command = {}
        command['code'] = code
        command['data'] = data
        return json.dumps(command)
    
    def heartbeat_request(self,msg):
        return self.pack_command(COMMAND_CODE['heartbeat_reply'])
    
    def heartbeat_reply(self,msg):
        print ('is alive!')
       
    
    def subscription_topic_request(self,topic_name):
        return self.pack_command(COMMAND_CODE['subscription_topic'],topic_name)

    def subscription_topic(self,msg):
        return self.pack_command(COMMAND_CODE['subscription_topic_reply'])

    def create_publisher_request(self,topic_name):
        return self.pack_command(COMMAND_CODE['create_publisher'],topic_name)

    def create_publisher(self,msg):
        return self.pack_command(COMMAND_CODE['create_publisher_reply'])

    def get_heart_beat_request_command(self):
        return self.pack_command(COMMAND_CODE['heartbeat_request'])
    
    def get_publish_topic_command(self,topic_name,msg_str):
        code = COMMAND_CODE['publish_topic']
        data = {}
        data['topic_name'] = topic_name
        data['msg_str'] = msg_str
        return self.pack_command(code,data)

    
    def publish_topic(self):
        return self.pack_command(COMMAND_CODE['publish_topic_reply'])
        
    def parser_msg(self,msg):
        try:
            command = json.loads(msg)
            #print (command)
            return self.haddle_dict[command['code']](msg)
        except Exception as e:
            print (e)
            return None
        
    def add_command_handle(self,code,handle):
        self.haddle_dict[code] = handle
        
        
    
    def get_walk_command(self):
        return self.pack_command(COMMAND_CODE['walk'])
        

if __name__=="__main__":
    cs = CommandSys()
    msg = cs.get_heart_beat_request_command()
    print (msg)
    msg = cs.parser_msg(msg)
    print (msg)
    msg = cs.parser_msg(msg)
    print (msg)
    
