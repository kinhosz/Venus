from vBase import *
from socket import *
from threading import Thread
import rsa
import time

# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


class callistoClient:
    def __init__(self, addr=("localhost", 12000)):
        self.__addr = addr
        self.__clientSocket = socket(AF_INET, SOCK_STREAM)
        self.__clientSocket.connect(addr)
        self.__msgReceived = False
        t = Thread(target=self.__recvMessage, args=(self.__clientSocket,))
        t.start()

    def getMessage(self):
        while self.__msgReceived == False:
            time.sleep(0.1)
        return self.__response

    def __recvMessage(self, clientSocket):
        message = clientSocket.recv(1024)
        clientSocket.close()
        self.__response = message
        self.__msgReceived = True

    def send(self, msg):
        self.__clientSocket.send(msg)


class vClient(vBase):
    def __init__(self):
        super().__init__()
        self.__serverKeys = {}
        self.__serverAuth = {}
        print("criei")
    # funcoes privadas

    def __getPublicKey(self, addr):
        encryptKey = self._CAKey
        decryptKey = self._CAKey
        msg = str(addr)
        response = self._sendCrypto(addr, msg, encryptKey, decryptKey)
        publicServerKey = response.split('\n')[1]
        hostname = response.split('\n')[0]
        if hostname != addr:
            return __getPublicKey(addr)
        return publicServerKey

    def __connect(self, addr):
        msg = "007" + '\n' + str(self.__publicKey)
        encryptKey = self.__serverKeys[addr]
        decryptKey = self.__privateKey
        response = self.__sendCrypto(addr, msg, encryptKey, decryptKey)
        return response

    def __assertConnection(self, addr):
        if addr not in self.__serverKeys.keys():
            publicKey = self.__getPublicKey(addr)
            self.__serverKeys[addr] = publicKey
            authKey = self.__connect(addr)
            self.__serverAuth[addr] = authKey

    def createSession(self, addr, description, options, endingMode="votes", limit=5):
        self.__assertConnection(addr)
        authKey = self.__serverAuth[addr]

        details = [
            authKey,
            "001",
            endingMode,
            str(limit),
            description
        ]
        msg = '\n'.join(details + options)

        encryptKey = self.__serverKeys[addr]
        decryptKey = self.__privateKey
        response = self.__sendCrypto(addr, msg, encryptKey, decryptKey)
        if response == "-1":
            print("An error occurred during the process")
        else:
            print("Sucessfully create session with ID " + response)

        return response

    def vote(self, addr, sessionID, option):
        self.__assertConnection(addr)

    def checkResult(self, addr, sessionID):
        self.__assertConnection(addr)

    def sayHi(self):
        print("hi")
