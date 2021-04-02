from socket import *
from threading import Thread


class callistoServer:

    def __init__(self, serverIP="localhost", serverPort=12000, capacity=100):
        self.__serverIP = serverIP
        self.__serverPort = serverPort
        self.__capacity = capacity

    def start(self):
        self.__serverSocket = socket(AF_INET, SOCK_STREAM)
        self.__serverSocket.bind((self.__serverIP, self.__serverPort))
        self.__serverSocket.listen(self.__capacity)

        while True:
            connectionSocket, addr = self.__serverSocket.accept()
            t = Thread(target=self.__respond, args=(connectionSocket, addr,))
            t.start()

    def __respond(self, con, cli):

        msg = ""
        while msg == "":
            msg = con.recv(1024).decode("utf-8")
        print(msg)

        con.send(bytes("NOT OK", "utf-8"))
        con.close()


if __name__ == "__main__":
    obj = callistoServer()
    obj.start()
