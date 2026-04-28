import random

# Stephanie Abundio
# msgCrypto.py 
#implementation of Diffie-Hellman -- finding the shared key  


class msgCrypto:

    prime=23 #predefined prime for simulation 
    g=5 #g of prime 

    def __init__(self):#constructors 
        self._private=self._privatekey()#sets private key 
        self._save_key=None

    #private key's method generator
    def _privatekey(self):
        return random.randint(2, self.prime-2)


    # punlic key's method generator 
    def gen_public(self):
        return pow(self.g,self._private)%self.prime
    
    def shared_key(self,key):
        return pow(key,self._private)%self.prime
        


    def diffie_hellman(self,other):  
        # Modulo with positive integers
            #print(10 % 3);

        sk=0

        a_pk=self.gen_public()
        b_pk=other.gen_public()

        a_sk=self.shared_key(b_pk)
        b_sk=other.shared_key(a_pk)

        if (a_sk==b_sk):
            sk=a_sk
        else: 
            return ("invalid")
        
        self._save_key=sk
        return sk
    

    #getter method 
    @property
    def save_key(self):
        return self._save_key 
    

     
    #alice = msgCrypto() 
    #bob = msgCrypto()

    #print(alice.diffe_hellman(bob))
        



        


        






        