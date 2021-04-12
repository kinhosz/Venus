# DEPENDENCIES
import random
import json
import rsa
import datetime
import socket
# PACKAGE CA
from Venus.Crypto.crypto import *
from Venus.TCP.callisto import *


class vServer():

    def __init__(self):
        # super().__init__()
        self.__clientAuth = {}
        self.__sessions = {}
        self.__CAKey = rsa.PublicKey(
            109250418308419214252988158234054746310229615585736037507546066195584397168016272841796091176995733151598575577605605009612419783247025738841944363988793837123448345186370466753697839705410912543140229146561184474662676112358669857389955427895692147640574974483494340547706839941457181394779357981284678316851, 65537)
        self.__CAaddr = (gethostbyname("localHost"), 1234)
        self.__myAddr = (gethostbyname("localHost"), 12000)
        (pubKey, privKey) = rsa.newkeys(1024)
        self.__publicKey = pubKey
        self.__privateKey = privKey

    # funcoes privadas

    def __getPK(self, R):

        if R not in self.__clientAuth.keys():
            return None

        return self.__clientAuth[R]

    def __handleResponse(self, data):
        data = decrypt(data, self.__privateKey)
        pkt = json.loads(data.decode("utf-8"))

        if pkt["code"] == "007":
            pkt = self.__handleConnect(pkt)
            pubKey = self.__getPK(pkt["auth"])

        data = json.dumps(pkt).encode("utf-8")
        data = encrypt(data, pubKey)
        return data

    def __handleConnect(self, pkt):

        authKey = random.randint(0, 1000000000000000000)
        pubKey = rsa.PublicKey(pkt["n"], pkt["e"])
        self.__clientAuth[authKey] = pubKey
        pkt = {}
        pkt["code"] = "907"
        pkt["auth"] = authKey

        return pkt

    def __handleCreateSession(self, description, options, endingMode, limit):
        sessionID = random.randint(0, 1000000)
        session = {}
        session["description"] = description
        session["options"] = options
        session["id"] = sessionID
        session["endingMode"] = endingMode
        session["limit"] = limit
        session["totalVotes"] = 0
        session["start"] = datetime.datetime.now()
        votes = []
        for i in range(len(options)):
            votes.append(0)
        session["votes"] = votes
        self.__sessions[sessionID] = session

        return sessionID

    def __handleVote(self, sessionID, option):

        if sessionID not in self.__sessions.keys():
            return "-1"

        session = self.__sessions[sessionID]

        if session["endingMode"] == "votes" and session["totalVotes"] == session["limit"]:
            return "-1"

        duration = (datetime.datetime.now() - session["start"]).totalseconds()

        if duration > session["limit"]:
            return "-1"

        pos = 0
        for e in session["options"]:
            if e == option:
                session["votes"][pos] = session["votes"][pos] + 1
                session["totalVotes"] = session["totalVotes"] + 1
                break
            pos = pos + 1

        self.__sessions[sessionID] = sessions

    def __handleCheckResult(self, sessionID):

        if sessionID not in self.__sessions.keys():
            return "-1"

        session = self.__sessions[sessionID]

        if session["endingMode"] == "votes" and session["totalVotes"] < session["limit"]:
            return "-1"

        duration = (datetime.datetime.now() - session["start"]).totalseconds()

        if duration < session["limit"]:
            return "-1"

        result = []

        for i in range(0, len(session["options"])):
            result.append((session["options"][i], session["votes"][i]))

        return result

    # funcoes publicas

    def register(self):
        channel = callistoClient(self.__CAaddr)
        pkt = {}
        pkt["code"] = "000"
        pkt["addr"] = self.__myAddr
        pkt["n"] = self.__publicKey.n
        pkt["e"] = self.__publicKey.e
        data = encrypt(json.dumps(pkt).encode("utf-8"), self.__CAKey)
        data = channel.send(data)
        if data == b'':
            print("no response")
        else:
            data = decrypt(data, self.__privateKey).decode("utf-8")
            pkt = json.loads(data)
            print(pkt["code"])

    def listen(self, lifetime=60):
        print("server ativo")
        channel = callistoServer(
            self.__handleResponse, self.__myAddr, lifetime=lifetime)
        channel.start()
