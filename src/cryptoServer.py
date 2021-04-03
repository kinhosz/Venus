import rsa
from socket import *
from threading import Thread


class callistoServer:

    def __init__(self,  privateKey, addr=("localhost", 3300), capacity=100):
        self.__serverAddr = addr
        self.__capacity = capacity
        self.__privateKey = privateKey

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

        msg = rsa.decrypt(packet, self.__privateKey)
        print(msg[0])

        con.close()


def main():

    (pubKey, privateKey) = rsa.newkeys(2048)
    print(pubKey)

    channel = callistoServer(privateKey)
    channel.start()


if __name__ == "__main__":
    main()
