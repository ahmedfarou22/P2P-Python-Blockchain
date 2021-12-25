import hashlib

class Block:
    def __init__(self,index,time_stamp,data,previous_hash):
        self.index = index
        self.time_stamp = time_stamp
        self.data = data
        self.previous_hash = previous_hash
        
    def __str__(self) -> str:
        return str( "{" "index: " + str(self.index) + " , " + " time_stamp: " + str(self.time_stamp) + " , " + " data: " + str(self.data) + " , " + " Previous-hash: "  + str(self.previous_hash) + "}")
    
    def __hash_block__(self):
        header = str(self.index) + str(self.time_stamp) + str(self.data) + str(self.previous_hash)
        inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
        outer_hash = hashlib.sha256(inner_hash).hexdigest()
        return outer_hash



class Chain:
    def __init__(self):
        self.Chain = []
        self.Chain.append(Block(1,"12:00","the_first_block_data","A00"))
    
    
    def __last_block__(self):
        return self.Chain[-1]
    
    def __create_block__(self,data):
        new_block = Block(len(self.Chain)+1, "2:00", data ,self.Chain[-1].__hash_block__())
        self.Chain.append(new_block)
    


        
        
ch1 = Chain()

ch1.__create_block__("nd block")
ch1.__create_block__("nd block ")
ch1.__create_block__("nd block")


for i in range(0,4):
    print(ch1.Chain[i])

# ch1.Chain[1]

ch1.Chain[1] = Block(99, "2:99", "edited block" ,ch1.Chain[-1].__hash_block__())

for i in range(0,4):
    print(ch1.Chain[i])
