import socket   #for sockets
import sys  #for exit
import blocksv2
import time
import hashlib

pendingtransactions = []
difficulty = 5

class Block:
    def __init__ (self,timestamp, data, previousHash,nonce):
        self.nonce = nonce
        self.timestamp  = timestamp
        self.data = data
        self.previousHash = previousHash   
        self.Hash = hashlib.sha256((self.data + ' ' + self.previousHash +' ' + str(self.nonce)).encode()).hexdigest()
    def __str__(self):
        return "************************************\n timestamp:    {0.timestamp}\n data:         {0.data}\n previousHash: {0.previousHash}\n hash:         {0.Hash}\n nonce:        {0.nonce}".format(self)


class Data:
    def __init__(self,fromaddress,toaddress,amount,signature):
        self.fromaddress = fromaddress
        self.toaddress = toaddress
        self.amount = amount
        self.signature = signature
    def __str__(self):
        return "From: {0.fromaddress}; To: {0.toaddress}; Amount: {0.amount}; Signature: {0.signature}".format(self)

try:
    #create an AF_INET, STREAM socket (TCP)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except (socket.error, msg):
    print( 'Failed to create socket. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1])
    

print ('Socket Created, connecting to host...')

host = '173.34.154.61'
port = 6666

print("ip address is " + host + ':' + str(port))


try:
    s.connect((host,6666))
    print("connected to " + host + " on ip " + host +  ' on ' + str(port))
except TimeoutError:
    print('Connection timed out, try again later')



def sendmsg(message):
    s.send(message.encode())
    reply = s.recv(4096)
    print(reply)
    
def givekey():
    key = blocksv2.RSA.generate(1024)
    print('public key is:  ' + blocksv2.encode62(key.e))
    print('private key is: ' + blocksv2.encode62(key.d))
    
    
def sendmoney(fromaddress,toaddress,amount,signature):
    blocksv2.createtransaction(Data(fromaddress,toaddress,amount,signature))
    s.send(blocksv2.pendingtostr().encode())
    reply = s.recv(4096)
    print (reply)

def minepending(myaddress):
    s.send('q'.encode())
    print('sent')
    reply = s.recv(4096)
    print(reply)
    transactions = ' '.join(reply.decode().split())
    print(transactions + ' as transaction received\n')
    s.send('w'.encode())
    reply = s.recv(4096)
    previoushash = ' '.join(reply.decode().split())
    print(previoushash + ' as hash received\n')
    newnonce = blocksv2.mineblock(difficulty,Block(time.strftime("%H:%M:%S", time.gmtime()), (transactions + ' '), previoushash, 0))
    s.send(('+' + myaddress + ' ' + str(newnonce)).encode())
    print(str(newnonce) + ' ' 'request sent')
    reply = s.recv(4096)
    print(reply)
    

    
