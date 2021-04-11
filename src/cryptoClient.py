import rsa
from socket import *
from threading import Thread
import time
import json
import sys


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


def encrypt(data, pubKey):
    response = bytes(0)
    block = rsa.common.byte_size(pubKey.n) - 11
    end = len(data)
    initial = 0
    while initial < end:
        finish = min(initial+block, end)
        response = response + rsa.encrypt(data[initial:finish], pubKey)
        initial = initial + block
    return response


def decrypt(data, privKey):
    response = bytes(0)
    block = rsa.common.byte_size(privKey.n)
    end = len(data)
    initial = 0
    while initial < end:
        finish = min(initial+block, end)
        response = response + rsa.decrypt(data[initial:finish], privKey)
        initial = initial + block
    return response


def main():

    (pubKey, privKey) = rsa.newkeys(1024)  # 245
    packet = {}
    packet["code"] = "008"
    packet["username"] = "kinho"
    packet["password"] = "1234"
    packet["pubKey"] = [pubKey.n, pubKey.e]
    message = json.dumps(packet)
    print(message)
    data = message.encode("utf-8")
    data = encrypt(data, pubKey)
    # print(data)
    print("-------------")
    data = decrypt(data, privKey)
    message = data.decode("utf-8")
    print(message)


if __name__ == "__main__":
    main()
