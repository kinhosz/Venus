from socket import *
from threading import Thread


class callistoClient:

    def __init__(self, serverIP="localhost", serverPort=12000):
        self.__serverIP = serverIP
        self.__serverPort = serverPort
        self.__clientSocket = socket(AF_INET, SOCK_STREAM)
        self.__clientSocket.connect((serverIP, serverPort))
        t = Thread(target=self.__recvMessage, args=(self.__clientSocket,))
        t.start()
        self.send("ola raparigas")

    def __recvMessage(self, clientSocket):

        message = clientSocket.recv(1024).decode("UTF-8")
        clientSocket.close()
        self.__response = message
        print(message)

    def send(self, msg):
        self.__clientSocket.send(bytes(msg, "utf-8"))


if __name__ == "__main__":

    lista = ["maria",
             "joao",
             str(34)]
    msg = '\n'.join(lista)
    print(msg[:-1])
