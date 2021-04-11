import rsa
import json

(pubKey, privKey) = rsa.newkeys(1024)
crypto = {}
crypto["privKey"] = {}
crypto["privKey"]["n"] = privKey.n
crypto["privKey"]["e"] = privKey.e
crypto["privKey"]["d"] = privKey.d
crypto["privKey"]["p"] = privKey.p
crypto["privKey"]["q"] = privKey.q

data = json.dumps(crypto)

f = open("privKey.txt", "w")
f.write(data)
f.close()

crypto.clear()
f = open("pubKey.txt", "w")
crypto["pubKey"] = {}
crypto["pubKey"]["n"] = privKey.n
crypto["pubKey"]["e"] = privKey.e
data = json.dumps(crypto)

f.write(data)
f.close()
