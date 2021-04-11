#from vBase import *
from socket import *
from threading import Thread
import rsa
import json
from TCP.web import callistoServer
# from CAKeys import *

# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


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


class vCA():

    def __init__(self):
        f = open("CA/CAKey.txt", "r")
        keys = json.loads(f.read())
        f.close()
        self.__publicKey = rsa.PublicKey(
            keys["privKey"]["n"], keys["privKey"]["e"])
        self.__privateKey = rsa.PrivateKey(
            keys["privKey"]["n"], keys["privKey"]["e"], keys["privKey"]["d"], keys["privKey"]["p"], keys["privKey"]["q"])
        # super().__init__(pubKey, privKey)
        self.__database = {}
        self.__CAaddr = ("localHost", 1234)
        print("CA online")

    def __encrypt(self, msg, encryptKey):

        encryptedMsg = rsa.encrypt(msg.encode("utf-8"), encryptKey)
        return encryptedMsg

    def __decrypt(self, msg, decryptKey):
        decryptedMsg = (rsa.decrypt(msg, decryptKey)).decode("utf-8")
        return decryptedMsg

    def __sendKey(self, IP):
        pass

    def __register(self, addr, pubKey):

        print("recebi o comando de registro")
        addr = msg["addr"]
        n = msg["n"]
        e = msg["e"]
        f = open("CA/database.txt", "r")
        database = json.loads(f.read())
        f.close()
        database[addr] = {}
        database[addr]["n"] = n
        database[addr]["e"] = e
        f = open("database.txt", "w")
        f.write(json.dumps(database))
        f.close()
        print("registrado")
        message = "REGISTRADO".encode("utf-8")
        return message

    def __handleResponse(self, packet):
        pkt = decrypt(packet, self.__privateKey)
        msg = json.loads(msg.decode("utf-8"))

        if(msg["code"] == "000"):
            return self.__register(msg)

    def listen(self):
        channel = callistoServer(self.__handleResponse, self.__CAaddr)
        print("ouvindo saporra")
        channel.start()
