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

        self.__callback(cli)
        con.close()


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

    def close(self):
        self.__clientSocket.close()
