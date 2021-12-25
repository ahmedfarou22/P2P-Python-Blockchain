import hashlib

class Block_Chain:
    def __init__(self) -> str:
        self.Chain = []
        first_block = self.__create_block__(1,"9:00","-","0000000000000000000000000000000000000000000000000000000000000000")
        self.Chain.append(first_block)
    
    def __create_block__(self,index,time_stamp,data,previous_hash) -> dict:
        nonce = 0
        
        header = str(index) + str(time_stamp) + str(data) + str(previous_hash) + str(nonce)
        
        inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
        outer_hash = hashlib.sha256(inner_hash).hexdigest()
        
        while outer_hash[:4] != "0000":
            nonce = nonce + 1
            header = str(index) + str(time_stamp) + str(data) + str(previous_hash) + str(nonce)
            inner_hash = hashlib.sha256(header.encode()).hexdigest().encode()
            outer_hash = hashlib.sha256(inner_hash).hexdigest()
        
        block = {
            "index":int(index),
            "time_stamp":str(time_stamp),
            "data":str(data),
            "previous_hash":str(previous_hash),
            "nonce":str(nonce),
            "hash":str(outer_hash)      
            }
        return block
    
    
    def __last_block__(self):
        return self.Chain[-1]
    


b1 = Block_Chain()

fistblock = b1.__create_block__(len(b1.Chain)+1,"9:01"," ",b1.__last_block__()["hash"])
b1.Chain.append(fistblock)

secondblock = b1.__create_block__(len(b1.Chain)+1,"9:02","-",b1.__last_block__()["hash"])
b1.Chain.append(secondblock)

thirdblock = b1.__create_block__(len(b1.Chain)+1,"9:03","-",b1.__last_block__()["hash"])
b1.Chain.append(thirdblock)


print(b1.Chain)

