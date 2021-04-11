import rsa


class vBase:

    def __init__(self, pubKey=(-1, -1), privKey=(-1, -1)):
        if privKey == (-1, -1):
            (pubKey, privKey) = rsa.newkeys(512)
        self._CAKey = rsa.PublicKey(
            109250418308419214252988158234054746310229615585736037507546066195584397168016272841796091176995733151598575577605605009612419783247025738841944363988793837123448345186370466753697839705410912543140229146561184474662676112358669857389955427895692147640574974483494340547706839941457181394779357981284678316851, 65537)
        self._CAaddr = ("localHost", 1234)
        self._publicKey = pubKey
        self._privateKey = privKey

    def _encrypt(self, msg, encryptKey):

        encryptedMsg = rsa.encrypt(msg.encode("utf-8"), encryptKey)
        return encryptedMsg

    def _decrypt(self, msg, decryptKey):
        decryptedMsg = (rsa.decrypt(msg, decryptKey)).decode("utf-8")
        return decryptedMsg
