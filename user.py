import sqlite3
from password import Password 
import hashlib

# Stephanie Abundio
# user.py 
''' creates database to store user information called users.db , here it hold the users full name, password and username
also acting as verify it checks on prexisting username to prevent repeats and 
verifies users password '''



class User: 

    DB_FILE="users.db"

    def __init__(self):
        #connects to database 
        self.conn=sqlite3.connect(self.DB_FILE)
        self.cursor=self.conn.cursor()

        #creating db if it doesnt exist
        self.cursor.execute("""
                            CREATE TABLE IF NOT EXISTS users(
                            username TEXT PRIMARY KEY, password TEXT,
                            salt TEXT, First TEXT, last TEXT
                            )
                            """)
        self.conn.commit()


    def register(self,first,last,username,password):

        if len(username)<=3:
            return "Username must be more than 3 characters"
        
        if len(password)<8:
            return "Password must be at least 8 characters "

        #check if username exist
        if self._checkuser(username):
            return "User already exist"
        
        
        p=Password()#creating obj password p
        p.set_password(password)#setting password 

        hashed=p.get_password() #get hash
        salt=p.get_salt()#get salt

        first=first
        last=last

        #insert to database 
        self.cursor.execute(
            "INSERT INTO users (username,password,salt,first,last) VALUES (?,?,?,?,?)",
            (username,hashed,salt,first,last)
        )
        self.conn.commit()

        return "Account created!"
    
    def login(self,username,password):

        self.cursor.execute(
            "SELECT password, salt FROM users WHERE username=?",
            (username,)
        )
        result=self.cursor.fetchone()#retrieving user info

        #if user exist
        if result:
            stored_hash,stored_salt=result

            combined=(stored_salt+password).encode()#combined salt + password and convert to bytes for hash
            hash_obj=hashlib.md5(combined)#hash obj md5
            rebuilt=hash_obj.hexdigest() #hash to hex string

            return rebuilt==stored_hash #compare if new hash is the same as previous hash
        
        return False #user not found
    
    def _checkuser(self,username):
        self.cursor.execute(
            "SELECT 1 FROM users WHERE username=?",
            (username,)
        )

        return self.cursor.fetchone() is not None
    
    
    
        
    





        










