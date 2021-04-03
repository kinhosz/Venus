import rsa
from socket import *
from threading import Thread


class callistoClient:
    def __init__(self, addr=("localhost", 3300)):
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


def main():

    (pubKey, privateKey) = rsa.newkeys(2048)
    print(pubKey)
    channel = callistoClient()
    msg = str(pubKey.n) + '\n' + str(pubKey.e)
    serverKey = rsa.PublicKey(17356696456326609787384458440264025691616143408621427405202879611221885123331580507634582285730172239855232170363195210578406972512452849674574809746546764158940136159884061481971247535275562821362984935452390519619213906265654199642147281036369385214646094355216119914908680962212744288239882578467886658416868551863058095807134889904437987579928321520414420942227387538869323254842039382009692723055089299080054098781220351964149416473379681195857414168732271350620219938605744443589474975619008283111308387473754995154617895847724310376804179409171850036400939429021173719363175742960909666215218788964798127604451, 65537)
    packet = rsa.encrypt(msg.encode("utf-8"), serverKey)
    channel.send(packet)


if __name__ == "__main__":
    main()
