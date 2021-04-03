import rsa


class vBase:

    def __init__(self, pubKey=(-1, -1), privKey=(-1, -1)):
        if privKey == (-1, -1):
            (pubKey, privKey) = rsa.newkeys(512)
        self._CAKey = rsa.PublicKey(
            9200098114067439893634252140694355402476065038057577832491289712454979621988673580646001426136915291374632007837644298362420129596328369545189941125667281, 65537)
        self._CAaddr = ("localHost", 1234)
        self._publicKey = pubKey
        self._privateKey = privKey

    def _encrypt(self, msg, encryptKey):

        encryptedMsg = rsa.encrypt(msg.encode("utf-8"), encryptKey)
        return encryptedMsg

    def _decrypt(self, msg, decryptKey):
        decryptedMsg = (rsa.decrypt(msg, decryptKey)).decode("utf-8")
        return decryptedMsg
