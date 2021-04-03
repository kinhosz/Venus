from vBase import *
from socket import *
from threading import Thread
import rsa
#from CAKeys import *

# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


class callistoServer:

    def __init__(self, callback, addr=("localhost", 12001), capacity=100):
        self.__serverAddr = addr
        self.__capacity = capacity
        self.__callback = callback

    def start(self):
        self.__serverSocket = socket(AF_INET, SOCK_STREAM)
        self.__serverSocket.bind(self.__serverAddr)
        self.__serverSocket.listen(self.__capacity)

        while True:
            connectionSocket, addr = self.__serverSocket.accept()
            t = Thread(target=self.__respond, args=(connectionSocket, addr,))
            t.start()

    def __respond(self, con, cli):

        packet = ""
        while packet == "":
            packet = con.recv(1024)
        print("mandei p callback")
        packet = self.__callback(packet)
        con.send(packet)
        con.close()


class vCA(vBase):

    def __init__(self):
        pubKey = rsa.PublicKey(
            9200098114067439893634252140694355402476065038057577832491289712454979621988673580646001426136915291374632007837644298362420129596328369545189941125667281, 65537)
        privKey = rsa.PrivateKey(9200098114067439893634252140694355402476065038057577832491289712454979621988673580646001426136915291374632007837644298362420129596328369545189941125667281, 65537,
                                 8666793679391726874180866665581093334117632838237922703546809348422197103308067049985045124029574778045820967296669608427821790249023217177492972175355273, 5553078155508246191122451036122831994342880202036572444916533741593251205066658571, 1656756461268533997893463677142406777858547858518431535785665826061013011)
        super().__init__(pubKey, privKey)
        self.__database = {}

    def __sendKey(self, IP):
        pass

    def __register(self, addr, pubKey):

        if addr in self.__database.keys():
            return "NOT OK"
        self.__database[addr] = pubKey
        return "OKKKKKK"

    def __handleResponse(self, packet):
        msg = self._decrypt(packet, self._privateKey)
        data = msg.split('\n')

        if(data[0] == "Register"):
            print("recebi o comando de registro")
            pubKey = data[2]
            print(pubKey)
            msg = self.__register(data[1], pubKey)
            print(msg)
            print("vou crip")
            packet = self._encrypt(msg, pubKey)
            print("cripei")
            return packet

    def listen(self):
        channel = callistoServer(self.__handleResponse, self._CAaddr)
        print("ouvindo saporra")
        channel.start()
