import rsa
(pubkey, privkey) = rsa.newkeys(512)
message = "pega porra".encode("UTF-*8")
crypto = rsa.encrypt(message, pubkey)
message = rsa.decrypt(crypto, pubkey)
message = message.decode("UTF-8")
