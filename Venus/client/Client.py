# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


class vClient():
    def __init__(self):
        # super().__init__()
        self.__CAKey = rsa.PublicKey(
            109250418308419214252988158234054746310229615585736037507546066195584397168016272841796091176995733151598575577605605009612419783247025738841944363988793837123448345186370466753697839705410912543140229146561184474662676112358669857389955427895692147640574974483494340547706839941457181394779357981284678316851, 65537)
        self._CAaddr = ("localHost", 1234)
        self.__serverKeys = {}
        self.__serverAuth = {}
        (pubKey, privKey) = rsa.newkeys(1024)
        self.__publicKey = pubKey
        self.__privateKey = privKey
        print("vClient pronto")
    # funcoes privadas

    def __sendCrypto(self, addr, msg, encryptKey=-1, decryptKey=-1):
        #encryptedMsg = self._encrypt(msg, encryptKey)
        channel = callistoClient(addr)
       # channel.send(encryptedMsg)
        channel.send(msg.encode("utf-8"))
        receivedMsg = channel.getMessage()
        #decryptedMsg = self._decrypt(msg, decryptKey)
        decryptedMsg = receivedMsg.decode("utf-8")
        return decryptedMsg

    def __getPublicKey(self, addr):
        encryptKey = self._CAKey
        decryptKey = self._CAKey
        msg = str(addr)
        response = self.__sendCrypto(self._CAaddr, msg, encryptKey, decryptKey)
        publicServerKey = response.split('\n')[1]
        hostname = response.split('\n')[0]
        if hostname != addr:
            return __getPublicKey(addr)
        return publicServerKey

    def __connect(self, addr):
        msg = "007" + '\n' + str(self.__publicKey)
        encryptKey = self.__serverKeys[addr]
        decryptKey = self.__privateKey
        response = self.__sendCrypto(addr, msg, encryptKey, decryptKey)
        return response

    def __assertConnection(self, addr):
        if addr not in self.__serverKeys.keys():
            publicKey = self.__getPublicKey(addr)
            self.__serverKeys[addr] = publicKey
            authKey = self.__connect(addr)
            self.__serverAuth[addr] = authKey

    def createSession(self, addr, description, options, endingMode="votes", limit=5):
        self.__assertConnection(addr)
        authKey = self.__serverAuth[addr]

        details = [
            authKey,
            "001",
            endingMode,
            str(limit),
            description
        ]
        msg = '\n'.join(details + options)

        encryptKey = self.__serverKeys[addr]
        decryptKey = self.__privateKey
        response = self.__sendCrypto(addr, msg, encryptKey, decryptKey)
        if response == "-1":
            print("An error occurred during the process")
        else:
            print("Sucessfully create session with ID " + response)

        return response

    def vote(self, addr, sessionID, option):
        self.__assertConnection(addr)
        authKey = self.__serverAuth[addr]

        details = [
            authKey,
            "002",
            sessionID,
            option
        ]
        msg = '\n'.join(details)
        response = self.__sendCrypto(addr, msg)
        if reponse.split('\n')[1] == 0:
            print(response.split('\n')[0] + " Sucessuful")
        else:
            print(response.split('\n')[0] + response.split('\n')[2])

    def checkResult(self, addr, sessionID):
        self.__assertConnection(addr)
        authKey = self.__serverAuth[addr]

        details = [
            authKey,
            "003",
            sessionID
        ]
        msg = '\n'.join(details)

        response = self.__sendCrypto(addr, msg)

        L = []
        data = response.split('\n')

        for i in range(2, len(data)):
            L.append(data[i])

        if response.split('\n')[1] == "-1":
            print(response.split('\n')[0] + " erro ao checar resultados")
        else:
            print(response.split('\n')[0] + " finalizado.")
            return L

    def sayHi(self):
        print("hi")
