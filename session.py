from msgCrypto import msgCrypto
from stream import stream 
from user import User
import os
import json
import time

# 
# session.py 
#creation of json file that stores users conversations
#decryption and encryption of message occurs here 

class Session: 

    LOG_FILE="messages.json"

    def __init__(self):
        self.logged_in_user=None
        self.shared_key=None
        self.is_authenticated=False
        self._user=User()
        self.active_recipient=None
        self._crypto={}#strore msg Crypto per user

        #checks if file exist if not create 
        if not os.path.exists(self.LOG_FILE):
            with open(self.LOG_FILE,"w") as f:
                json.dump({},f,indent=4)
        
    

    def authenticate(self,username,password):

        hold=self._user.login(username,password)

        if hold: 
            self.logged_in_user=username #setting user
            self.is_authenticated=True #they exist
            self._crypto[username]=msgCrypto() #user an object 
            return True
        
        if hold is False:
            return False
        
        

    def set_recipient(self,recipient):
        
        self.active_recipient=recipient

        if recipient not in self._crypto:
            self._crypto[recipient]= msgCrypto()

        self.establish_keys()

        

    def establish_keys(self):

        if self.is_authenticated is False:
            return "Error: wrong username or password"
        
        if self.active_recipient is None:
            return 1
        
        saved = self._load_key(self.logged_in_user, self.active_recipient)

        if saved:
            self.shared_key = saved 
        else:
            sender= self._crypto[self.logged_in_user] #msgCrypto obj
            recipient= self._crypto[self.active_recipient] #assign recipient for sender 

            self.shared_key=sender.diffie_hellman(recipient)#get key from diffie hellman method 
            self._save_key(self.logged_in_user, self.active_recipient, self.shared_key)

        return self.shared_key
    
    def _save_key(self, user1, user2, key):
        with open(self.LOG_FILE,"r") as f:
            data = json.load(f)

        if "keys" not in data:
            data["keys"] = {}

        pair = "_".join(sorted([user1, user2]))   # "alice_bobj" always same order
        data["keys"][pair] = key
        
        with open(self.LOG_FILE,"w") as f:
            json.dump(data, f, indent=2)

    def _load_key(self, user1, user2):
        with open(self.LOG_FILE,"r") as f:
            data = json.load(f)

        pair = "_".join(sorted([user1, user2]))
        return data.get("keys", {}).get(pair, None)

    def send_message(self,plaintext):

        if self.shared_key is None:
            return None #checks if key was establish
        
        if self.active_recipient is None:
            return None #checks if recipient exist
        
        #encrypt the message 
        secret= stream()

        ciphertext=secret.streamcipher(plaintext,self.shared_key)

        #save to file.json 

        with open(self.LOG_FILE,"r") as f:
            data=json.load(f)

        if self.logged_in_user not in data:
            data[self.logged_in_user]={"conversations":{}} #start conversations 

        if self.active_recipient not in data[self.logged_in_user]["conversations"]:
            data[self.logged_in_user]["conversations"][self.active_recipient]=[]#create conversation if logged in user never had one before 

        data[self.logged_in_user]["conversations"][self.active_recipient].append({
            "from": self.logged_in_user,
            "ciphertext":ciphertext,
            "timestamp":time.time()
        })

        if self.active_recipient not in data:
            data[self.active_recipient]={"conversations":{}} #start conversations if user did not have previous convo 

        if self.logged_in_user not in data[self.active_recipient]["conversations"]:
            data[self.active_recipient]["conversations"][self.logged_in_user]=[]#create conversation if logged in user never had one before 

        data[self.active_recipient]["conversations"][self.logged_in_user].append({
            "from": self.logged_in_user,
            "ciphertext":ciphertext,
            "timestamp":time.time()
        })

        with open(self.LOG_FILE,"w") as f:
            json.dump(data,f,indent=2)

        return ciphertext
    
    def receive_message(self,ciphertext):

        if self.shared_key is None:
            return None #no key was made
        
        secret=stream()#stream obj

        plaintext=secret.decrypt(ciphertext,self.shared_key)#decryption of ciphertext 

        return plaintext
    
    def get_conversations(self,recipient):

        with open(self.LOG_FILE,"r") as f:
            data=json.load(f)#loading data

            return data.get(self.logged_in_user,{}).get("conversations",{}).get(recipient,[])
        
    def get_conversations_from(self, sender, recipient):
    # reads messages stored under sender's account to recipient
        with open(self.LOG_FILE,"r") as f:
            data = json.load(f)
        return data.get(sender,{}).get("conversations",{}).get(recipient,[])




    def logout(self):
        self.logged_in_user=None
        self.shared_key= None
        self.is_authenticated=False
        self.active_recipient=None
        self._crypto={}

        





        

    
        
        


        






    