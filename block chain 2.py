import hashlib
import datetime

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
            "nonce":str("0"),
            "hash":str("")    
            }
    
    def __str__(self) -> str:
        return str(self.block)



class Block_Chain:
    def __init__(self) -> str:
        self.Chain = []
        first_block = Block(1,"0000-00-00 00:00:00.000000","00","00","00","0","0000000000000000000000000000000000000000000000000000000000000000")
        first_block.block["nonce"] = "11350"
        first_block.block["hash"] = "00002eed10f5a7c3c9ea3b3321412231633b87f390edbcd9905d5443921dc939"
        self.Chain.append(first_block)
    
    def __last_block__(self) -> Block:
        return self.Chain[-1]
    
    def __hash_function__(self,block) -> hash:
        header = str(block.block["index"]) + str(block.block["time_stamp"]) +str(block.block["sitting_number"]) +str(block.block["student_name"]) +str(block.block["subject"]) + str(block.block["data"])  + str(block.block["previous_hash"]) + str(block.block["nonce"])
        inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
        outer_hash = hashlib.sha256(inner_hash).hexdigest()
        return outer_hash
    
    def __create_block__(self,sitting_number,student_name,subject,data) -> Block:
        new_block = Block(len(self.Chain)+1,datetime.datetime.now(),str(sitting_number),str(student_name),str(subject),str(data),self.Chain[-1].block["hash"])
        
        hash = self.__hash_function__(new_block)
        
        new_block.block["hash"] = hash
        return new_block
    
    def __mine_block__(self,block_to_mine) -> Block:
        hash = block_to_mine.block["hash"]
        nonce = 0
        
        while hash[:4] != "0000":
            nonce = nonce + 1
            header = str(block_to_mine.block["index"]) + str(block_to_mine.block["time_stamp"])+str(block_to_mine.block["sitting_number"]) + str(block_to_mine.block["student_name"]) + str(block_to_mine.block["subject"]) + str(block_to_mine.block["data"]) + str(block_to_mine.block["previous_hash"]) + str(nonce)
            inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
            outer_hash = hashlib.sha256(inner_hash).hexdigest()
            hash = outer_hash
        
        block_to_mine.block["nonce"] = nonce
        block_to_mine.block["hash"] = outer_hash
        
        mined_bolck = block_to_mine
        return mined_bolck
    
    def __add_block_to_block_chain__(self,block_to_add) -> None:
        block_to_add_hash = block_to_add.block["hash"]
        
        if block_to_add_hash [:4] == "0000":
            if block_to_add.block["previous_hash"] == self.__last_block__().block["hash"]:
                self.Chain.append(block_to_add)
            
        else:
            print("your block is not mined or incorect")
            
    def __create_mine_add__(self,data) -> None:
        a = self.__create_block__(data)
        b = self.__mine_block__(a)
        self.__add_block_to_block_chain__(b)






b1 = Block_Chain()




for i in range(len(b1.Chain)):
    print(b1.Chain[i])

