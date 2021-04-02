from vBase import *


# Requisição da chave pública de algum nó do cliente para o CA:
# Resposta do CA para requisições de chave pública:
# Requisição da Autenticação do cliente para o servidor:
# Resposta da autenticação do cliente
# Requisição da operação do cliente
# Resposta da operação do cliente


class vServer(vBase):

    def __init__(self):
        super().__init__()
        self.__clientAuth = {}
    # funcoes privadas

    def __handleConnect(self, clientKey):
        pass

    def __handleCreateSession(self, IP, description, options, endingMode, limit):
        pass

    def __handleVote(self, IP, sessionID, option):
        pass

    def __handleCheckResult(self, IP, sessionID):
        pass

    # funcoes publicas

    def listen(self):
        pass
