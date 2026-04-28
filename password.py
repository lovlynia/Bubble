
import hashlib
import os
from typing import Union 

#Stephanie Abundio
#Hash Algorithms for Password Configuration 
#using md5 and salt

class Password: 
    
    def __init__(self):
        self._storepassword=None
        self._salt=None


    #Standardizes inpute to bytes 
    def to_bytes(self,data:Union[str,bytes])->bytes:
        return data.encode("utf-8") if isinstance(data,str) else data


    def md5(self,data: Union[str,bytes])-> str:
        b=self.to_bytes(data)#conversion to bytes stored into b
        h=hashlib.md5()#hash object
        h.update(b)#updates hash 
        return h.hexdigest()#returns hexadecimal of hash text
    
    def generate_salt(self):
        return os.urandom(16).hex() #os bring 16 random bytes defined as hex 
    
    def set_password(self,password:str): #setting password 
        self._salt=self.generate_salt() 
        salted=self._salt+password
        self._storepassword=self.md5(salted) #store salted password 

    def verify_password(self,password:str)->bool: #flagging true or false 
        salted=self._salt+password
        temp=self.md5(salted)

        if temp==self._storepassword:
            return True
        else: 
            return False


    def get_password(self):
        return self._storepassword #getter method for password 
    
    def get_salt(self):
        return self._salt #getter method for salt
    
    
        






