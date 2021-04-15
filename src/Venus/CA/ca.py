# DEPENDENCIES
import time
import random
import json
import rsa
import datetime
# PACKAGE CA
from Venus.Crypto.crypto import *
from Venus.TCP.callisto import *
# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


class vCA():

    def __init__(self):
        self.__CAKEY = "Venus/CA/data/CAKey.txt"
        self.__CA_DATABASE = "Venus/CA/data/database.txt"
        f = open(self.__CAKEY, "r")
        keys = json.loads(f.read())
        f.close()
        self.__publicKey = rsa.PublicKey(
            keys["privKey"]["n"], keys["privKey"]["e"])
        self.__privateKey = rsa.PrivateKey(
            keys["privKey"]["n"], keys["privKey"]["e"], keys["privKey"]["d"], keys["privKey"]["p"], keys["privKey"]["q"])
        f = open(self.__CA_DATABASE, "r")
        self.__database = json.loads(f.read())
        f.close()
        self.__CAaddr = (keys["addr"]["ip"], keys["addr"]["port"])
        print("CA online")

    def __register(self, addr, n, e):

        user = str(addr[0]) + "::" + str(addr[1])
        self.__database[user] = {}
        self.__database[user]["n"] = n
        self.__database[user]["e"] = e
        pkt = {}
        pkt["code"] = "900"
        return pkt

    def __getKey(self, addr):
        user = str(addr[0]) + "::" + str(addr[1])

        if user not in self.__database.keys():
            return None

        pubKey = rsa.PublicKey(
            self.__database[user]["n"], self.__database[user]["e"])
        return pubKey

    def __handleResponse(self, packet):

        packet = decrypt(packet, self.__privateKey)
        msg = json.loads(packet.decode("utf-8"))

        if msg["code"] == "000":
            addr = msg["addr"]
            msg = self.__register(addr, msg["n"], msg["e"])
            pubKey = self.__getKey(addr)

        elif msg["code"] == "001":
            addr = msg["addr"]
            pubKey = rsa.PublicKey(msg["n"], msg["e"])
            ret = self.__getKey(addr)

            if ret == None:
                msg = {}
                msg["code"] = "901"
            else:
                msg = {}
                msg["code"] = "900"
                msg["addr"] = addr
                msg["n"] = ret.n
                msg["e"] = ret.e
        else:
            msg = {}
            msg["code"] = "901"

        pkt = json.dumps(msg).encode("utf-8")
        pkt = encrypt(pkt, pubKey)
        return pkt

    def __close(self):
        f = open(self.__CA_DATABASE, "w")
        txt = json.dumps(self.__database)
        f.write(txt)
        f.close()

    def listen(self, lifetime=None):
        channel = callistoServer(
            self.__handleResponse, self.__CAaddr, lifetime=lifetime)
        print("Servidor ouvindo em ", str(self.__CAaddr))
        channel.start()
        self.__close()
        print("closed")
