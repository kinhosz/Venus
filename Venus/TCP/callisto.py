# DEPENDENCIES
import time
from socket import *
from threading import Thread


class callistoServer:

    def __init__(self, callback, addr=("localhost", 3300), capacity=100, lifetime=10):
        self.__serverAddr = addr
        self.__capacity = capacity
        self.__callback = callback
        self.__lifetime = lifetime

    def start(self):
        self.__serverSocket = socket(AF_INET, SOCK_STREAM)
        self.__serverSocket.bind(self.__serverAddr)
        self.__serverSocket.listen(self.__capacity)
        self.__serverSocket.settimeout(self.__lifetime)

        alive = True
        while alive:
            try:
                connectionSocket, addr = self.__serverSocket.accept()
                print("connected with ", str(addr))
                t = Thread(target=self.__respond,
                           args=(connectionSocket, addr,))
                t.start()
            except:
                alive = False

        self.__serverSocket.close()

    def __respond(self, con, cli):

        packet = ""
        while packet == "":
            packet = con.recv(1024)

        data = self.__callback(packet)
        con.send(data)
        con.close()


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

        message = ""
        while message == "":
            try:
                message = clientSocket.recv(1024)
            except:
                self.__response = b''
                self.__msgReceived = True

        clientSocket.close()
        self.__response = message
        self.__msgReceived = True

    def send(self, msg):
        self.__clientSocket.send(msg)
        while self.__msgReceived == False:
            time.sleep(0.1)
        return self.__response
