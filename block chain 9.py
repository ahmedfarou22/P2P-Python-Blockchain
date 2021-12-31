import hashlib, datetime, json, socket, threading, random, time

from cryptography.fernet import Fernet # used for symmetric encryption 

############# Block, BlockChain, And P2P Classes #############
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
        
        
    def binarySearch(self,arr, l, r, x):
        # Check base case
        if r >= l:
    
            mid = l + (r - l) // 2
    
            # If element is present at the middle itself
            if arr[mid].block["index"] == x:
                return mid
    
            # If element is smaller than mid, then it
            # can only be present in left subarray
            elif arr[mid].block["index"] > x:
                return self.binarySearch(arr, l, mid-1, x)
    
            # Else the element can only be present
            # in right subarray
            else:
                return self.binarySearch(arr, mid + 1, r, x)
    
        else:
            # Element is not present in the array
            return -1
    
    def encrypt_data(self,plain_data):
        key = Fernet.generate_key()
        x = key.decode()
        print("--> this is the key of the block do not forget it: " + str(x))
        f = Fernet(key)
        encrypted_text = f.encrypt(bytes(plain_data, "UTF-8"))
        return encrypted_text.decode()


    def decrypt_data(self,encrypted_data):
        key = input("please enter the key: ")
        f = Fernet(key)
        return f.decrypt(bytes(encrypted_data,"UTF-8")).decode()
    
    
    def __hash_function__(self,block) -> hash:
        header = str(block.block["index"]) + str(block.block["time_stamp"]) +str(block.block["sitting_number"]) +str(block.block["student_name"]) +str(block.block["subject"]) + str(block.block["data"])  + str(block.block["previous_hash"]) + str(block.block["nonce"])
        inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
        outer_hash = hashlib.sha256(inner_hash).hexdigest()
        return outer_hash
    
    def __create_block__(self,sitting_number,student_name,subject,data) -> Block:
        new_block = Block(str(len(self.Chain)+1),datetime.datetime.now(),str(sitting_number),str(student_name),str(subject),self.encrypt_data(data),self.Chain[-1].block["hash"])
        
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
            
    # def __create_mine_add__(self,sitting_number,student_name,subject,data) -> None: # for testing only 
    #     a = self.__create_block__(sitting_number,student_name,subject,data)
    #     b = self.__mine_block__(a)
    #     self.__add_block_to_block_chain__(b)


class Peer_To_Peer:
    def __init__(self) -> str:
        self.my_ip = self.__get_real_ip__()
        self.my_port = 6666 # static port
        
        self.ip_list = [self.my_ip]
        self.port_list = [self.my_port]
        
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.my_ip, self.my_port))
        self.server.listen()
    
    def __get_real_ip__(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        real_ip = s.getsockname()[0]
        s.close()
        return real_ip
    
    def dict_to_block(self,dictt) -> Block:
        a_block = Block(dictt["index"],dictt["time_stamp"],dictt["sitting_number"],dictt["student_name"],dictt["subject"],dictt["data"],dictt["previous_hash"])
        a_block.block["data"] = dictt["data"]
        a_block.block["nonce"] = dictt["nonce"]
        a_block.block["hash"] = dictt["hash"]
        return a_block
    
    def broadcast_block(self,block): 
        for q in range(1,len(self.ip_list)):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((self.ip_list[q], self.port_list[q]))
                json_block_dict = json.dumps(block.block)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
            
            except:
                pass
    
    def send_random_string(self,string): 
        for i in range(0,30):
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                randomclient = random.randint(1,len(self.ip_list)-1) #should start at one becouse the random person should never be the same person
                client.connect((self.ip_list[randomclient], self.port_list[randomclient]))
                json_string = json.dumps(string)
                client.send(json_string.encode('utf-8'))
                client.close()
                break
            except:
                continue
            
    def send_random_block(self,block): # sends a block to random person
        while True:
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                randomclient = random.randint(1,len(self.ip_list)-1) #should start at one becouse the random person should never be the same person
                client.connect((self.ip_list[randomclient], self.port_list[randomclient]))
                json_block_dict = json.dumps(block.block)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
                break
            except:
                continue


class Node(object):
    def __init__(self, value: int, next_node: "Node" = None):
        self.value = value
        self.next = next_node

    def __repr__(self):
        return "Node <{}>".format(self.value)

class Queue(object):
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value: int) -> None:
        new_node = Node(value)

        if self.head is None:
            self.head = new_node
            self.tail = self.head
            return

        self.tail.next = new_node
        self.tail = new_node 

    def dequeue(self) -> int:
        try:
            value = self.head.value
            self.head = self.head.next

            if self.head is None:
                self.tail = None

            return value
        except:
            print("--> deque is empty")
            pass

    def is_empty(self):
        return self.head is None
    
    def isnotEmpty(self):
        if self.head is not None:
            return True
    
    def first(self):
        return self.head.value

############# Initiating 2 Objects #############

b1 = Block_Chain()
network = Peer_To_Peer()
q1 = Queue()

############# Main program starts here 2 functions in Threading #############

def receive():
    while True:
        client, address = network.server.accept()
        somthing_sent = client.recv(1024)
        decoded_somthing = somthing_sent.decode()
        receved = json.loads(decoded_somthing)
        
        if type(receved) is dict:
            receved_block = network.dict_to_block(receved)
            q1.enqueue(receved_block)

            

            if q1.isnotEmpty():
                if q1.first().block["hash"][:4] != "0000":
                    minded_block = b1.__mine_block__(q1.first())
                    if minded_block.block["previous_hash"] == b1.Chain[-1].block["hash"]:
                        b1.__add_block_to_block_chain__(minded_block)
                        network.broadcast_block(minded_block) #brodcast  the minded block
                        print("--> I was choosen at random to proof a block. I proofed the block and the block is broadcasted")
                        q1.dequeue()
                    
                    else:
                        print("--> I was choosen at random to proof the block but its previous hash does not match my previous hash")
                        q1.dequeue()
                        
            if q1.isnotEmpty():
                if q1.first().block["hash"][:4] == "0000":
                    if q1.first().block["previous_hash"] == b1.Chain[-1].block["hash"]:
                        b1.__add_block_to_block_chain__(q1.first())
                        print("--> I receved a minded block I compared the hash with the previos and added it")
                        q1.dequeue()
                    else:
                        print("--> I receved a minded block that does not match")
                        q1.dequeue()
                    

        
        if type(receved) is str:
            if receved == "send latest":
                new_list=[]
                ip, _sent_port = address
                index = network.ip_list.index(str(ip))
                for i in range(len(b1.Chain)):
                    block = b1.Chain[i]
                    dict_from_block = block.block
                    new_list.append(dict_from_block)
                
                for k in range(1,len(new_list)): # start at one to not send the first block
                    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    client.connect((network.ip_list[index], network.port_list[index]))
                    dictr = json.dumps(new_list[k])
                    client.send(dictr.encode('utf-8'))
                    client.close()
            
            if receved[:10] == "j--network":
                ip = receved[10:]
                send = ("add" + ip)
                for i in range(1,len(network.ip_list)):
                    try:
                        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        client.connect((network.ip_list[i], network.port_list[i]))
                        json_sss = json.dumps(send)
                        client.send(json_sss.encode('utf-8'))
                        client.close()
                    except:
                        pass
                if str(ip) not in network.ip_list:
                    network.ip_list.append(str(ip))
                    network.port_list.append(6666)
                
                lsend = ("l-add" + network.my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,6666))
                json_lsend = json.dumps(lsend)
                client.send(json_lsend.encode('utf-8'))
                client.close()
                
            
            if receved[:3] == "add":
                ip = receved[3:]
                if str(ip) not in network.ip_list:
                    network.ip_list.append(str(ip))
                    network.port_list.append(6666)
                
                lsend = ("l-add" + network.my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip,6666))
                last_add = json.dumps(lsend)
                client.send(last_add.encode('utf-8'))
                client.close()
            
            if receved[:5] == "l-add":
                ip = receved[5:]
                if str(ip) not in network.ip_list:
                    network.ip_list.append(str(ip))
                    network.port_list.append(6666)

def menu():
    while True:
        print("= = = = = = = = = Menu = = = = = = = = =")
        print("1.type create --> to create a new block")
        print("2.type see    --> to see the curent version of blockcahin you have")
        print("3.type search name --> to search the block chain by name")
        print("3.type search number --> to search the block chain by sitting number")
        print("4.type search index --> to search the block chain by index")
        print("5.type full data  --> to previw the data of a block on the block chain")
        print("6.type join --> to join the P2P network")
        print("7.type peers --> to see all the peers on the network")
        print("8.type update --> to update your block chain")
        print("9.type exit  --> to exit the program")
        inputt = input("What whould you like to do : \n")

        if inputt == "create":
            print("Please add information to the block : ")
            one =  str(input("What is the student's sitting number : "))
            two =  str(input("What is the student's name : "))
            three =  str(input("What is the subject : "))
            four = str(input("please atatch the test : "))
            created_block = b1.__create_block__(one,two,three,four)

            network.send_random_block(created_block)
            print("--> Block created")
            print("--> your block is sent for proofing")

        elif inputt == "see":
            print(b1)
        
        if inputt == "search name":
            name_looking_for = str(input("Please enter the name of the student you are looking for: "))
            print(b1.get_block_by_name(name_looking_for))

        if inputt == "search number":
            setting_number_looking_for = str(input("Please enter the sitting number of the student you are looking for: "))
            print(b1.get_block_by_sitting_number(setting_number_looking_for))
        
        if inputt == "search index":
            index_looking_for = int(input("Please enter the index of the block you are looking for: "))
            index_of_block_Chain = b1.binarySearch(b1.Chain, 0, len(b1.Chain) -1 , index_looking_for)
            print(b1.Chain[index_of_block_Chain])
        
        if inputt == "full data":
            index_looking_for = int(input("Please enter the index of the block you are looking for: "))
            index_of_block_Chain = b1.binarySearch(b1.Chain, 0, len(b1.Chain) -1 , index_looking_for)
            blokaya = b1.Chain[index_of_block_Chain]
            print("Decrypted Data: " + b1.decrypt_data(blokaya.block["data"]))
        
        if inputt == "join":
            if len(network.ip_list) == 1:
                ip_input = str(input("Please enter an Ip of a node on the network: "))
                j_send = ("j--network" + network.my_ip)
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((ip_input,6666))
                json_block_dict = json.dumps(j_send)
                client.send(json_block_dict.encode('utf-8'))
                client.close()
                time.sleep(2) # Sleep for 2 seconds before geting last version of the block cahin
                network.send_random_string("send latest")
            if len(network.ip_list) > 1:
                print("--> you are now on the network")
            
        if inputt == "peers":
            print(network.ip_list)
        
        if inputt == "update":
            network.send_random_string("send latest")

        if inputt == "exit":
            break



receive_thread = threading.Thread(target=receive)
receive_thread.start()

menu_thread = threading.Thread(target=menu)
menu_thread.start()
