# DEPENDENCIES
import json
import rsa
# PACKAGE CA
from Venus.Crypto.crypto import *
from Venus.TCP.callisto import *
# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente

# code
"""
 return a packet from server
 a timeout code is represented by 408 code
"""


class vClient():
    def __init__(self):
        # super().__init__()
        self.__CAKey = rsa.PublicKey(
            109250418308419214252988158234054746310229615585736037507546066195584397168016272841796091176995733151598575577605605009612419783247025738841944363988793837123448345186370466753697839705410912543140229146561184474662676112358669857389955427895692147640574974483494340547706839941457181394779357981284678316851, 65537)
        self.__CAaddr = (gethostbyname("localHost"), 1234)
        self.__serverKeys = {}
        self.__serverAuth = {}
        (pubKey, privKey) = rsa.newkeys(1024)
        self.__publicKey = pubKey
        self.__privateKey = privKey
        print("vClient pronto")
    # funcoes privadas

    def __isValid(self, pkt, code):

        if pkt["code"] == code:
            return pkt
        else:
            print("error: ", pkt["code"])
            return None

    def __connect(self, addr):
        pubKey = self.__getServerPK(addr)
        user = str(addr[0]) + "::" + str(addr[1])
        pkt = {}
        pkt["code"] = "007"
        pkt["n"] = self.__publicKey.n
        pkt["e"] = self.__publicKey.e
        data = json.dumps(pkt).encode("utf-8")
        data = encrypt(data, pubKey)
        channel = callistoClient(addr)
        data = channel.send(data)
        if data == b'':
            print("no response")
            return None

        data = decrypt(data, self.__privateKey)
        pkt = json.loads(data.decode("utf-8"))
        pkt = self.__isValid(pkt, "907")
        if pkt == None:
            return None

        R = pkt["auth"]
        self.__serverAuth[user] = R

    def __assertConnection(self, addr):
        user = str(addr[0]) + "::" + str(addr[1])
        if user not in self.__serverAuth.keys():
            self.__connect(addr)

    def createSession(self, addr, description, options, endingMode=1, limit=5):
        self.__assertConnection(addr)
        authKey = self.__getServerAuth(addr)

        pkt = {
            "auth": authKey,
            "code": "001",
            "endingMode": endingMode,
            "limit": limit,
            "description": description,
            "options": options
        }

        pubKey = self.__getServerPK(addr)
        data = json.dumps(pkt).encode("utf-8")
        data = encrypt(data, pubKey)
        channel = callistoClient(addr)
        data = channel.send(data)

        if data == b'':
            pkt = {
                "code": "408"
            }
            return pkt

        data = decrypt(data, self.__privateKey)
        pkt = json.loads(data.decode("utf-8"))
        return pkt

    def vote(self, addr, sessionID, option):
        self.__assertConnection(addr)
        auth = self.__getServerAuth(addr)
        pkt = {
            "auth": auth,
            "code": "002",
            "sessionID": sessionID,
            "option": option
        }

        pubKey = self.__getServerPK(addr)
        data = json.dumps(pkt).encode("utf-8")
        data = encrypt(data, pubKey)
        channel = callistoClient(addr)
        data = channel.send(data)
        if data == b'':
            pkt = {
                "code": "408"
            }
            return pkt

        data = decrypt(data, self.__privateKey)
        pkt = json.loads(data.decode("utf-8"))
        return pkt

    def checkResult(self, addr, sessionID):
        self.__assertConnection(addr)
        auth = self.__getServerAuth(addr)
        pkt = {
            "auth": auth,
            "code": "003",
            "sessionID": sessionID
        }

        pubKey = self.__getServerPK(addr)
        data = json.dumps(pkt).encode("utf-8")
        data = encrypt(data, pubKey)
        channel = callistoClient(addr)
        data = channel.send(data)
        if data == b'':
            pkt = {
                "code": "408"
            }
            return pkt

        data = decrypt(data, self.__privateKey)
        pkt = json.loads(data.decode("utf-8"))
        return pkt

    def __getServerAuth(self, addr):
        user = str(addr[0]) + "::" + str(addr[1])
        return self.__serverAuth[user]

    def __getServerPK(self, addr):
        user = str(addr[0]) + "::" + str(addr[1])
        if user in self.__serverKeys.keys():
            return self.__serverKeys[user]

        channel = callistoClient(self.__CAaddr)
        pkt = {}
        pkt["code"] = "001"
        pkt["addr"] = addr
        pkt["n"] = self.__publicKey.n
        pkt["e"] = self.__publicKey.e
        data = json.dumps(pkt).encode("utf-8")
        data = encrypt(data, self.__CAKey)
        data = channel.send(data)

        if data == b'':
            print("no response")
            return None

        data = decrypt(data, self.__privateKey).decode("utf-8")
        pkt = json.loads(data)

        if pkt["code"] == "900" and pkt["addr"][0] == addr[0] and pkt["addr"][1] == addr[1]:
            pubKey = rsa.PublicKey(pkt["n"], pkt["e"])
            self.__serverKeys[user] = pubKey
            return pubKey
        else:
            return None

    def sayHi(self):

        print("hi")
