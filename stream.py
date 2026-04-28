import random 
# Stephanie Abundio
# stream.py 
#implementation of Stream Cipher -- Encrypt and Decrypt functions 



class stream:

    def streamcipher(self,plaintext,shared):

        keystream=[(i*shared+3)% 256 for i in range(len(plaintext))]# generating pseudo 

        ciphertext=[]# array for construction of cipher text 

        for i in range(len(plaintext)):
            # for i in rand by length of my pt
            c=ord(plaintext[i])^keystream[i]# convert to ascii and xor values plaintext and key stream
            ciphertext.append(c)

        return ciphertext
    
    def decrypt(self,ciphertext,shared):
        keystream=[(i*shared+3)% 256 for i in range(len(ciphertext))]# generating pseudo 

        plaintext=""# array for construction of cipher text 

        for i in range(len(ciphertext)):
            # for i in rand by length of my pt
            p=ciphertext[i]^keystream[i]
            plaintext+=chr(p)

        return plaintext







        
