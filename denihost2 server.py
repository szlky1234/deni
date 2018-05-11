import time
import socket
import threading
import sys
import blocksv2
import hashlib

difficulty = 5
class Data:
    def __init__(self,fromaddress,toaddress,amount,signature):
        self.fromaddress = fromaddress
        self.toaddress = toaddress
        self.amount = amount
        self.signature = signature
    def __str__(self):
        return "From: {0.fromaddress}; To: {0.toaddress}; Amount: {0.amount}; Signature: {0.signature}".format(self)

class Block:
    def __init__ (self,timestamp, data, previousHash,nonce):
        self.nonce = nonce
        self.timestamp  = timestamp
        self.data = data
        self.previousHash = previousHash   
        self.Hash = hashlib.sha256((self.timestamp + ' '+ self.data + ' ' + self.previousHash +' ' + str(self.nonce)).encode()).hexdigest()
    def __str__(self):
        return "************************************\n timestamp:    {0.timestamp}\n data:         {0.data}\n previousHash: {0.previousHash}\n hash:         {0.Hash}\n nonce:        {0.nonce}".format(self)
class Server:
    sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    nodes = ['173.34.154.61']
    ports = [5555]        
    connections = []
    print('starting server')
    def __init__(self):
        
        self.sock.bind(('0.0.0.0',6666))
        self.sock.listen(5)
        print('socket binded')
        
    def handler(self,c,a):
        while True:
            data = c.recv(4096)
            print(data.decode())
            split = data.decode().split()
            if not data:
                print(str(a[0]) + ':' + str(a[1]) + ' disconnected')
                self.connections.remove(c)
                c.close()
                break
            
            elif len(split) == 4:
                if split[0][0] == '*':
                    if blocksv2.checksignature(split[3],split[2],split[0][1:]):
                        blocksv2.createtransaction(Data(split[0][1:],split[1],split[2],split[3]))
                        print('pending added with amount: ' + split[2])
                        c.send(('pending added with amount: ' + split[2]).encode())
                    elif not blocksv2.checksignature(split[3],split[2],split[0][1:]):
                        print('signature invalid')
                        c.send(('signature is invalid').encode())
                         
            elif split[0][0] == '!':
                print('checking balance of: ' + split[0][1:] + '\n')
                b = blocksv2.checkbal(split[0][1:])
                print(b)
                c.send(('this user has ' + str(b) + ' denicoins').encode())
            elif len(split) == 2:
                
                if split[0][0]== '+':
                    newhash = hashlib.sha256((blocksv2.pendingtostr() + ' ' + blocksv2.getlastblock().Hash + ' ' + split[1]).encode()).hexdigest()
                    if (newhash)[0:difficulty] == '0' * difficulty:
                        f = open('chain.txt','a')
                        f.writelines(blocksv2.returnpending())
                        f.close()   
                        blocksv2.addblock2(Block(time.strftime("%H:%M:%S", time.gmtime()), blocksv2.pendingtostr(), 'aaa', split[1]), newhash, split[0][1:])
                        c.send(('new block added, hash:' + blocksv2.getlastblock().Hash + '\n').encode())
                        print('adding new block', 'hash ' + newhash)    
                    else:
                        c.send('invalid hash\n'.encode())
                        print('invalid\n')
                
            elif split[0][0] == 'r':
                blocksv2.readchain() 
                c.send('readchain request received\n'.encode())
            elif split[0] == 'ping':
                c.send('pong!'.encode())
            elif split[0][0] == 'w':
                c.send((blocksv2.getlastblock().Hash).encode())
                print('last hash sent\n')
            elif split[0][0] == 'q':
                c.send(blocksv2.pendingtostr().encode())
                print('pending sent\n')

            else:
                print(data.decode())
                print('i dont understand')
                c.send((data.decode() + " is an invalid command\n").encode())                
                
    def run(self):
        print('ran')
        while True:
            c,a = self.sock.accept()
            cThread = threading.Thread(target = self.handler, args = (c,a))
            cThread.daemon = True
            cThread.start()
            self.connections.append(c)
            print(str(a[0]) + ':' + str(a[1]) + ' connected')

server = Server()
server.run()

            
