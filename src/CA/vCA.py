from vBase import *
from socket import *
from threading import Thread
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

        msg = ""
        while msg == "":
            msg = con.recv(1024)

        self.__callback(msg, addr)
        con.close()


class vCA(vBase):

    def __init__(self):
        pubKey = CApubKey
        privKey = CAprivKey
        super().__init__(pubKey, privKey)
        print(self._publicKey)
        print(self._privateKey)

    def __sendKey(self, IP):
        pass

    def __handleResponse(self):
        print("oi")

    def listen(self):
        channel = callistoServer(self.__handleResponse)
        channel.start()
