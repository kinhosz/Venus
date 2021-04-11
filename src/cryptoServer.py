import rsa
from socket import *
from threading import Thread
import time


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

        decrypt = rsa.PublicKey(
            6910515391195348810132447251178670692951059336858946790607328386601007565781193579517590880812544951865837954471821768623160793092926852029297019945858141, 65537)
        packet = rsa.decrypt(packet, decrypt)
        msg = packet.decode("utf-8")
        print(msg)

        con.close()


def main():

    (pubKey, privateKey) = rsa.newkeys(512)

    channel = callistoServer(privateKey)
    channel.start()


if __name__ == "__main__":
    main()
