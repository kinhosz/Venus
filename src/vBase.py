import rsa
from CA.CAKeys import *


class vBase:

    def __init__(self, pubKey=(-1, -1), privKey=(-1, -1)):
        if privKey == (-1, -1):
            (pubKey, privKey) = rsa.newkeys(512)
        self._CAKey = CApubKey
        self._CAaddr = ("localHost", 1234)
        self._publicKey = pubKey
        self._privateKey = privKey

    def _sendCrypto(self, addr, msg, encryptKey, decryptKey):
        encryptedMsg = rsa.encrypt(msg.encode("utf-8"), encryptKey)
        channel = callistoClient(addr)
        channel.send(encryptedMsg)
        receivedMsg = channel.getMessage()
        decryptedMsg = (rsa.decrypt(receveidMsg, decryptKey)).decode("utf-8")
        return decryptedMsg
