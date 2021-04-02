from vBase import *
from socket import *
from threading import Thread


class callistoServer:

    def __init__(self, callback, addr=("localhost", 12000), capacity=100):
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


class vServer(vBase):

    def __init__(self):
        super().__init__()
        self.__clientAuth = {}
    # funcoes privadas

    def __handleResponse(self, msg, addr):
        print("oi")

    def __handleConnect(self, clientKey):
        pass

    def __handleCreateSession(self, IP, description, options, endingMode, limit):
        pass

    def __handleVote(self, IP, sessionID, option):
        pass

    def __handleCheckResult(self, IP, sessionID):
        pass

    # funcoes publicas

    def listen(self):
        channel = callistoServer(self.__handleResponse)
        channel.start()
