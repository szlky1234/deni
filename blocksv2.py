import time
import hashlib
from hashlib import blake2b
from hashlib import blake2s
import threading
from Crypto.PublicKey import RSA


pendingtransactions = []

class Block:
    def __init__ (self,timestamp, data, previousHash,nonce):
        self.nonce = nonce
        self.timestamp  = timestamp
        self.data = data
        self.previousHash = previousHash   
        self.Hash = hashlib.sha256((self.data + ' ' + self.previousHash +' ' + str(self.nonce)).encode()).hexdigest()
    def __str__(self):
        return "************************************\n timestamp:    {0.timestamp}\n data:         {0.data}\n previousHash: {0.previousHash}\n hash:         {0.Hash}\n nonce:        {0.nonce}".format(self)
    
def creategenesis():
    return Block(time.strftime("%H:%M:%S", time.gmtime()), '' ,'0',0)

class Data:
    def __init__(self,fromaddress,toaddress,amount,signature):
        self.fromaddress = fromaddress
        self.toaddress = toaddress
        self.amount = amount
        self.signature = signature
    def __str__(self):
        return "From: {0.fromaddress}; To: {0.toaddress}; Amount: {0.amount}; Signature: {0.signature}".format(self)
Blockchain = [creategenesis()]

def checkhash(newhash,difficulty):
    hashlib.sha256().hexdigest()
    hashlib.sha256((time.strftime("%H:%M:%S", time.gmtime()) + ' '+ pendingtostr() + ' ' + 
                    getlastblock().Hash + ' ' + str()).encode()).hexdigest()    
    return None

def getlastblock():
    return Blockchain[len(Blockchain) - 1]

def addblock(newblock):
    newblock.previousHash = getlastblock().Hash
    newblock.Hash = hashlib.sha256((newblock.data + ' '  + newblock.previousHash + ' '+ str(mineblock(4,newblock))).encode()).hexdigest()
    newblock.data = pendingtostr()
    Blockchain.append(newblock)
    
def addblock2(newblock,newhash,recipient):
    global pendingtransactions
    newblock.previousHash = getlastblock().Hash
    newblock.Hash = newhash
    newblock.data = pendingtostr()
    Blockchain.append(newblock)
    pendingtransactions = [Data('server',recipient,'30','signature')]
    
def readchain():
    for i in range (0,len(Blockchain)):
        print (Blockchain[i])

def ischainvalid():
    for i in range(0,len(Blockchain)-1):
        if Blockchain[i].Hash != Blockchain[i+1].previousHash:
            return False
        elif Blockchain[i].Hash == Blockchain[i+1].previousHash:
            return True
    
    
def mineblock(difficulty,newblock):
    while hashlib.sha256((newblock.data + ' ' + newblock.previousHash +' ' + str(newblock.nonce)).encode()).hexdigest()[0:difficulty] != '0' * difficulty:
        newblock.nonce = newblock.nonce + 1
        hashlib.sha256((newblock.data + ' ' + 
                        newblock.previousHash + ' ' + str(newblock.nonce)).encode()) 
    
    print (hashlib.sha256((newblock.data + ' ' + 
                        newblock.previousHash + ' ' + str(newblock.nonce)).encode()).hexdigest())
    return (newblock.nonce)

def pendingtostr():
    empty = ''
    for i in pendingtransactions:
        empty = empty + i.fromaddress + ' ' + i.toaddress + ' ' + i.amount + ' ' + i.signature + ' '
    return empty

def minepending(myaddress):
    global pendingtransactions
    addblock(Block(time.strftime("%H:%M:%S", time.gmtime()), pendingtostr(), 'aaa', 0))
    pendingtransactions = [Data('server',myaddress,'30','signature')]
    print ('block mined, hash: ' + getlastblock().Hash)
    print('nonce : ' + str(getlastblock().nonce))

def createtransaction(Data):
    pendingtransactions.append(Data)
    

def returnpending():
    empty = []
    for i in pendingtransactions:
        string = i.fromaddress +' ' +i.toaddress + ' '+ i.amount + ' ' + i.signature + '\n'
        empty.append(string)
    return empty

def testmine(difficulty,string):
    while hashlib.sha256((str(string)).encode()).hexdigest()[0:difficulty] != '0' * difficulty:
        string = string + 1
        hashlib.sha256(str(string).encode())
    print(str(string))
    return hashlib.sha256(str(string).encode()).hexdigest()

BASE62 = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
def encode62(num, alphabet=BASE62):
    """Encode a positive number in Base X

    Arguments:
    - `num`: The number to encode
    - `alphabet`: The alphabet to use for encoding
    """
    if num == 0:
        return alphabet[0]
    arr = []
    base = len(alphabet)
    while num:
        num, rem = divmod(num, base)
        arr.append(alphabet[rem])
    arr.reverse()
    return ''.join(arr)

def decode62(string, alphabet=BASE62):
    """Decode a Base X encoded string into the number

    Arguments:
    - `string`: The encoded string
    - `alphabet`: The alphabet to use for encoding
    """
    base = len(alphabet)
    strlen = len(string)
    num = 0

    idx = 0
    for char in string:
        power = (strlen - (idx + 1))
        num += alphabet.index(char) * (base ** power)
        idx += 1
    return num

def checksignature(signature,amount,fromn):
    if fromn == 'server':
        return True
    elif amount == str(pow(decode62(signature),65537,decode62(fromn))):
        return True
    else:
        return False

def checkbal(fromn):
    total = 0
    for i in Blockchain[1:]:
        for data in range(0,len(i.data.split())):
            if (i.data.split())[data] == fromn:
                if data == 0:
                    total = total - int((i.data.split())[2])
                elif data % 4 == 0:
                    total = total - int((i.data.split())[data+2])
                else:
                    total = total + int((i.data.split())[data+1])
    return total 

createtransaction(Data('alice','bob','0','signature'))
#createtransaction(Data(encode62(alicekey.n),encode62(bobkey.n),'10', encode62(pow(10,alicekey.d,alicekey.n))))
#createtransaction(Data(encode62(stevekey.n),encode62(rogerkey.n),'20', encode62(pow(20,stevekey.d,stevekey.n))))
#createtransaction(Data(encode62(stevekey.n),encode62(alicekey.n),'50', encode62(pow(50,stevekey.d,stevekey.n))))