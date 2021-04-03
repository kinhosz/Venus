from vBase import *
from socket import *
from threading import Thread
import time
import random
import datetime


class callistoClient:
    def __init__(self, addr=("localhost", 12000)):
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


class callistoServer:

    def __init__(self, callback, addr=("localhost", 3300), capacity=100):
        self.__serverAddr = addr
        self.__capacity = capacity
        self.__callback = callback

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

        self.__callback(packet, addr)
        con.close()


class vServer(vBase):

    def __init__(self):
        super().__init__()
        self.__clientAuth = {}
        self.__sessions = {}

    # funcoes privadas

    def __handleResponse(self, packet, addr):
        msg = packet.decode("utf-8")
        authKey = msg.split('\n')[0]
        data = msg.split('\n')[1:]

        if data[0] == "007":
            return self.__handleConnect(data[1])

        if authKey not in self.__clientAuth.keys():
            return "NULL"

        if data[0] == "001":
            size = data[4]
            options = []
            for i in range(5, 5+size):
                options.append(data[i])

            return self.__handleCreateSession(endingMode=data[1], limit=data[2], description=data[3], options=options)
        elif data[0] == "002":
            return self.__handleVote(data[1], data[2])
        elif data[0] == "003":
            return self.__handleCheckResult(data[1])

    def __handleConnect(self, clientKey):

        authKey = random.randint(0, 1000000000)

        self.__clientAuth[authKey] = clientKey

        return authKey

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

    def listen(self):
        channel = callistoServer(self.__handleResponse)
        channel.start()
