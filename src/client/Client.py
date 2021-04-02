from vBase import *


# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


class vClient(vBase):

    def __init__(self):
        super().__init__()
        self.__serverKeys = {}
        self.__serverAuth = {}
    # funcoes privadas

    def __sendCrypto(self, IP, publicKey, auth, msg):
        pass

    def __getPublicKey(self, IP):
        pass

    def __connect(self, IP):
        pass

    def __assertConnection(IP):

        if IP not in self.__serversKeys.keys():
            publicKey = self.__getPublicKey(IP)
            self.__serverKeys[IP] = publicKey
            authKey = self.__connect(IP)
            self.__serverAuth[IP] = authKey

    def createSession(self, IP, description, options, endingMode="votes", limit=5):
        pass

    def vote(self, IP, sessionID, option):
        pass

    def checkResult(self, IP, sessionID):
        pass
