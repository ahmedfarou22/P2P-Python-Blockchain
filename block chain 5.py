import hashlib, datetime, json, socket, threading, random, time

"""get my ip and static port"""
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
my_ip = s.getsockname()[0]
my_port = 6666 # static port
s.close()
"""''''''''''''''''''''''''''''"""


"""Start Server And Set list of IPs And Ports"""
ip_list = [my_ip]
port_list = [my_port]
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((my_ip, my_port))
server.listen()
"""''''''''''''''''''''''''''''"""


############# Block and Block Chain #############
class Block:
    def __init__(self,index,time_stamp,sitting_number,student_name,subject,data,previous_hash) -> None:
        self.index = index
        self.time_stamp = time_stamp
        self.sitting_number = sitting_number
        self.student_name = student_name
        self.subject = subject
        self.data = data
        self.previous_hash = previous_hash
        
        self.block = {
            "index":int(self.index),
            "time_stamp":str(self.time_stamp),
            "sitting_number":str(self.sitting_number),
            "student_name":str(self.student_name),
            "subject":str(subject),
            
            "data":str(self.data),
            
            "previous_hash":str(self.previous_hash),
            "nonce": 0,
            "hash":str("")    
            }
    
    def __str__(self) -> str:
        return str(self.block)

class Block_Chain:
    def __init__(self) -> str:
        self.Chain = []
        first_block = Block(1,"0000-00-00 00:00:00.000000","00","00","00","0","0000000000000000000000000000000000000000000000000000000000000000")
        first_block.block["hash"] = self.__hash_function__(first_block)
        self.__mine_block__(first_block)
        self.Chain.append(first_block)
    
    def __str__(self) -> str:
        for i in range(len(self.Chain)):
            print(str(self.Chain[i]))
        return str("")
    
    def __last_block__(self) -> Block:
        return self.Chain[-1]
    
    def get_block_by_name(self,name : str) -> Block:
        for i in range(len(self.Chain)):
            if self.Chain[i].block["student_name"] == name:
                return self.Chain[i]
        print("--> could not find the block associated with name you searched for")

    def get_block_by_sitting_number(self,sitting_number : str) -> Block:
        for i in range(len(self.Chain)):
            if self.Chain[i].block["sitting_number"] == sitting_number:
                return self.Chain[i]
        print("--> could not find the block associated with sitting number you searched for")


    def __hash_function__(self,block) -> hash:
        header = str(block.block["index"]) + str(block.block["time_stamp"]) +str(block.block["sitting_number"]) +str(block.block["student_name"]) +str(block.block["subject"]) + str(block.block["data"])  + str(block.block["previous_hash"]) + str(block.block["nonce"])
        inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
        outer_hash = hashlib.sha256(inner_hash).hexdigest()
        return outer_hash
    
    def __create_block__(self,sitting_number,student_name,subject,data) -> Block:
        new_block = Block(str(len(self.Chain)+1),datetime.datetime.now(),str(sitting_number),str(student_name),str(subject),str(data),self.Chain[-1].block["hash"])
        
        new_block.block["hash"] = self.__hash_function__(new_block)
        
        return new_block
    
    def __mine_block__(self,block_to_mine) -> Block:
        
        while block_to_mine.block["hash"][:4] != "0000":
            
            block_to_mine.block["nonce"] += 1
            block_to_mine.block["hash"] =  self.__hash_function__(block_to_mine)
            
        return block_to_mine
    
    def __add_block_to_block_chain__(self,block_to_add) -> None:
        block_to_add_hash = block_to_add.block["hash"]
        
        if block_to_add_hash [:4] == "0000":
            if block_to_add.block["previous_hash"] == self.__last_block__().block["hash"]:
                self.Chain.append(block_to_add)
            else:
                print("the block's previous hash is incorrect or not mined properly")
            
        else:
            print("your block is not mined or incorrect")
            
    def __create_mine_add__(self,sitting_number,student_name,subject,data) -> None:
        a = self.__create_block__(sitting_number,student_name,subject,data)
        b = self.__mine_block__(a)
        self.__add_block_to_block_chain__(b)


b1 = Block_Chain()



############# Peer To Peer Network #############
def dict_to_block(dictt) -> Block:
    a_block = Block(dictt["index"],dictt["time_stamp"],dictt["sitting_number"],dictt["student_name"],dictt["subject"],dictt["data"],dictt["previous_hash"])
    a_block.block["data"] = dictt["data"]
    a_block.block["nonce"] = dictt["nonce"]
    a_block.block["hash"] = dictt["hash"]
    return a_block

def broadcast_block(block): # broadcasts blocks
    for i in range(1,len(ip_list)):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((ip_list[i], port_list[i]))
            json_block_dict = json.dumps(block.block)
            client.send(json_block_dict.encode('utf-8'))
            client.close()
        except:
            pass

def send_random_string(string): #broadcasts strings
    for i in range(0,30):
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            randomclient = random.randint(1,len(ip_list)-1) #should start at one becouse the random person should never be the same person
            client.connect((ip_list[randomclient], port_list[randomclient]))
            json_string = json.dumps(string)
            client.send(json_string.encode('utf-8'))
            client.close()
            break
        except:
            continue
            
def send_random_block(block): # sends a block to random person
    while True:
        try:
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            randomclient = random.randint(1,len(ip_list)-1) #should start at one becouse the random person should never be the same person
            client.connect((ip_list[randomclient], port_list[randomclient]))
            json_block_dict = json.dumps(block.block)
            client.send(json_block_dict.encode('utf-8'))
            client.close()
            break
        except:
            continue

def receive():
    while True:
        client, address = server.accept()
        somthing_sent = client.recv(1024)
        decoded_somthing = somthing_sent.decode()
        receved = json.loads(decoded_somthing)
        
        if type(receved) is dict:
            receved_block = dict_to_block(receved)
            
            if receved_block.block["hash"][:4] != "0000":
                minded_block = b1.__mine_block__(receved_block)
                if minded_block.block["previous_hash"] == b1.Chain[-1].block["hash"]:
                    b1.__add_block_to_block_chain__(minded_block)
                    broadcast_block(minded_block) #brodcast  the minded block
                    print("--> I was choosen at random to proof a block. I proofed the block and the block is broadcasted")
                else:
                    print("--> I was choosen at random to proof the block but its previous hash does not match my previous hash")

            
            if receved_block.block["hash"][:4] == "0000":
                if receved_block.block["previous_hash"] == b1.Chain[-1].block["hash"]:
                    b1.__add_block_to_block_chain__(receved_block)
                    print("--> I receved a minded block I compared the hash with the previos and added it")
                else:
                    print("--> I receved a minded block that does not match")

            else:
                print("--> An unknown eroor")
        
        if type(receved) is str:
            if receved == "send latest":
                new_list=[]
                ip, _sent_port = address
                index = ip_list.index(str(ip))
                for i in range(len(b1.Chain)):
                    block = b1.Chain[i]
                    dict_from_block = block.block
                    new_list.append(dict_from_block)
                
                for k in range(1,len(new_list)): # start at one to not send the first block
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((ip_list[index], port_list[index]))
                    dictr = json.dumps(new_list[k])
                    client.send(dictr.encode('utf-8'))
                    client.close()
            
            if receved[:10] == "j--network":
                ip = receved[10:]
                send = ("add" + ip)
                for i in range(1,len(ip_list)):
                    try:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((ip_list[i], port_list[i]))
                        json_block_dict = json.dumps(send)
                        client.send(json_block_dict.encode('utf-8'))
                        client.close()
                    except:
                        pass
                if str(ip) not in ip_list:
                    ip_list.append(str(ip))
                    port_list.append(6666)
                
                lsend = ("l-add" + my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,6666))
                json_block_dict = json.dumps(lsend)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
                
            
            if receved[:3] == "add":
                ip = receved[3:]
                if str(ip) not in ip_list:
                    ip_list.append(str(ip))
                    port_list.append(6666)
                
                lsend = ("l-add" + my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,6666))
                json_block_dict = json.dumps(lsend)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
            
            if receved[:5] == "l-add":
                ip = receved[5:]
                if str(ip) not in ip_list:
                    ip_list.append(str(ip))
                    port_list.append(6666)



def menu():
    while True:
        print("= = = = = = = = = Menu = = = = = = = = =")
        print("1.type create --> to create a new block")
        print("2.type see    --> to see the curent version of blockcahin you have")
        print("3.type search name --> to search the block chain by name")
        print("3.type search number --> to search the block chain by sitting number")
        print("4.type join --> to join the P2P network")
        print("4.type peers --> to see all the peers on the network")
        print("5.type update --> to update your block chain")
        print("6.type exit  --> to exit the program")
        inputt = input("What whould you like to do : \n")
        
        if inputt == "create":
            print("Please add information to the block : ")
            one =  str(input("What is the student's sitting number : "))
            two =  str(input("What is the student's name : "))
            three =  str(input("What is the subject : "))
            four= str(input("What is the please atatch the test : "))
            
            created_block = b1.__create_block__(one,two,three,four)

            send_random_block(created_block)
            print("--> Block created")
            print("--> your block is sent for proofing")

        elif inputt == "see":
            print(b1)
        
        if inputt == "search name":
            name_looking_for = str(input("Please enter the name of the student you are looking for: "))
            print(b1.get_block_by_name(name_looking_for))

        if inputt == "search number":
            setting_number_looking_for = str(input("Please enter the name of the student you are looking for: "))
            print(b1.get_block_by_sitting_number(setting_number_looking_for))
        
        if inputt == "join":
            if len(ip_list) == 1:
                ip_input = str(input("Please enter an Ip of a node on the network: "))
                j_send = ("j--network" + my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip_input,6666))
                json_block_dict = json.dumps(j_send)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
                time.sleep(2) # Sleep for 2 seconds before geting last version of the block cahin
                send_random_string("send latest")
            if len(ip_list) > 1:
                print("--> you are already on the network")
            
        if inputt == "peers":
            print(ip_list)
        
        if inputt == "update":
            send_random_string("send latest")

        if inputt == "exit":
            break


############# Threading #############

receive_thread = threading.Thread(target=receive)
receive_thread.start()

menu_thread = threading.Thread(target=menu)
menu_thread.start()
